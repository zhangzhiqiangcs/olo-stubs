from mypy.nodes import (
    NameExpr, Expression, TypeInfo, Block, SymbolTableNode, Argument, Var, ARG_STAR2, MDEF, FuncBase, SymbolNode,
    FuncDef, ARG_POS, PassStmt, Decorator)
from mypy.plugin import (
    Plugin, FunctionContext, ClassDefContext, MethodContext)
from mypy.plugins.common import add_method
from mypy.semanal_shared import set_callable_name
from mypy.types import (
    UnionType, NoneTyp, Instance, Type, AnyType, TypeOfAny, CallableType,
    TypeVarDef, TypeType)
from mypy.typevars import fill_typevars
from mypy.util import get_unique_redefinition_name

try:
    from mypy.types import get_proper_type
except ImportError:
    get_proper_type = lambda x: x

from typing import Optional, Callable, Dict, List, TypeVar, Union

MYPY = False  # we should support Python 3.5.1 and cases where typing_extensions is not available.
if MYPY:
    from typing_extensions import Final, Type as TypingType

T = TypeVar('T')
CB = Optional[Callable[[T], None]]

CHECK_REQUIRED_METHOD_NAMES = frozenset(
    ['create']
)

ALL_METHOD_NAMES = CHECK_REQUIRED_METHOD_NAMES | {
    'get_by', 'gets_by', 'get_multi_by', 'update'
}

FIELD_NAME = 'olo.field.Field'  # type: Final[str]


# See https://github.com/python/mypy/issues/6617 for plugin API updates.

def fullname(x: Union[FuncBase, SymbolNode]) -> str:
    """Compatibility helper for mypy 0.750 vs older."""
    fn = x.fullname
    if callable(fn):
        return fn()
    return fn


def shortname(x: Union[FuncBase, SymbolNode]) -> str:
    """Compatibility helper for mypy 0.750 vs older."""
    fn = x.name
    if callable(fn):
        return fn()
    return fn


def is_model(info: TypeInfo) -> bool:
    """Check if this is a subclass of a declarative base."""
    if info.mro:
        for base in info.mro:
            metadata = base.metadata.get('olo')
            if metadata and metadata.get('model_base'):
                return True
    return False


def set_model(info: TypeInfo) -> None:
    """Record given class as a model base."""
    info.metadata.setdefault('olo', {})['model_base'] = True


class BasicOLOPlugin(Plugin):
    """Basic plugin to support simple operations with models.

    Currently supported functionality:
      * Recognize dynamically defined declarative bases.
      * Add an __init__() method to models.
      * Provide better types for 'Field's
    """
    def get_function_hook(self, fullname: str) -> Optional[Callable[[FunctionContext], Type]]:
        if fullname == FIELD_NAME:
            return field_hook
        sym = self.lookup_fully_qualified(fullname)
        if sym and isinstance(sym.node, TypeInfo):
            # May be a model instantiation
            if is_model(sym.node):
                return init_method_hook
        return None

    def get_method_hook(self, fullname: str) -> Optional[Callable[[MethodContext], Type]]:
        classname, _, method_name = fullname.rpartition('.')
        cls_sym = self.lookup_fully_qualified(classname)
        if cls_sym and isinstance(cls_sym.node, TypeInfo):
            if is_model(cls_sym.node) and method_name in ALL_METHOD_NAMES:
                check_required = method_name in CHECK_REQUIRED_METHOD_NAMES
                return generate_method_hook(cls_sym.node, check_required=check_required)
        return None

    def get_base_class_hook(self, fullname: str) -> 'CB[ClassDefContext]':
        sym = self.lookup_fully_qualified(fullname)
        if fullname == 'olo.model.Model' and isinstance(sym.node, TypeInfo):
            set_model(sym.node)
            return None
        if sym and isinstance(sym.node, TypeInfo):
            if is_model(sym.node):
                return add_model_init_hook
        return None


def add_var_to_class(name: str, typ: Type, info: TypeInfo) -> None:
    """Add a variable with given name and type to the symbol table of a class.

    This also takes care about setting necessary attributes on the variable node.
    """
    var = Var(name)
    var.info = info
    var._fullname = fullname(info) + '.' + name
    var.type = typ
    info.names[name] = SymbolTableNode(MDEF, var)


def add_model_init_hook(ctx: ClassDefContext) -> None:
    """Add a dummy __init__() to a model and record it is generated.

    Instantiation will be checked more precisely when we inferred types
    (using get_function_hook and model_hook).
    """
    if '__init__' in ctx.cls.info.names:
        # Don't override existing definition.
        return
    any = AnyType(TypeOfAny.special_form)
    var = Var('kwargs', any)
    kw_arg = Argument(variable=var, type_annotation=any, initializer=None, kind=ARG_STAR2)
    add_method(ctx, '__init__', [kw_arg], NoneTyp())
    ctx.cls.info.metadata.setdefault('olo', {})['generated_init'] = True


def generate_method_hook(model: TypeInfo, check_required: bool = False) -> Callable[[Union[FunctionContext, MethodContext]], Type]:
    def _(ctx: Union[FunctionContext, MethodContext]) -> Type:
        metadata = model.metadata.get('olo')
        if not metadata or not metadata.get('generated_init'):
            return ctx.default_return_type

        # Collect column names and types defined in the model
        # TODO: cache this?
        all_required_names = []
        expected_types = {}  # type: Dict[str, Type]
        for cls in model.mro[::-1]:
            for name, sym in cls.names.items():
                if not isinstance(sym.node, Var):
                    continue
                tp = get_proper_type(sym.node.type)
                if not isinstance(tp, Instance):
                    continue
                if fullname(tp.type) != FIELD_NAME:
                    continue
                # assert len(tp.args) == 1
                expected_types[name] = tp.args[0]
                if is_required_field(tp):
                    all_required_names.append(name)

        arg_names = ctx.arg_names[0]
        if len(ctx.arg_names) == 2:
            arg_names = ctx.arg_names[1]
        arg_types = ctx.arg_types[0]
        if len(ctx.arg_types) == 2:
            arg_types = ctx.arg_types[1]

        if check_required:
            arg_names_set = set(arg_names)
            required_names = [n for n in all_required_names if n not in arg_names_set]

            if required_names:
                ctx.api.fail('Required args: {} not provided'.format(', '.join(map('`{}`'.format, required_names))),
                             ctx.context)

        for actual_name, actual_type in zip(arg_names, arg_types):
            if actual_name is None:
                # We can't check kwargs reliably.
                # TODO: support TypedDict?
                continue
            if actual_name not in expected_types:
                ctx.api.fail('Unexpected field "{}" for model "{}"'.format(actual_name,
                                                                           shortname(model)),
                             ctx.context)
                continue
            # Using private API to simplify life.
            ctx.api.check_subtype(actual_type, expected_types[actual_name],  # type: ignore
                                  ctx.context,
                                  'Incompatible type for "{}" of "{}"'.format(actual_name,
                                                                              shortname(model)),
                                  'got', 'expected')
        return ctx.default_return_type

    return _


def init_method_hook(ctx: Union[FunctionContext, MethodContext]) -> Type:
    """More precise model instantiation check.

    Note: sub-models are not supported.
    Note: this is still not perfect, since the context for inference of
          argument types is 'Any'.
    """
    assert isinstance(ctx.default_return_type, Instance)  # type: ignore[misc]
    model = ctx.default_return_type.type
    return generate_method_hook(model, check_required=True)(ctx)


def get_argument_by_name(ctx: FunctionContext, name: str) -> Optional[Expression]:
    """Return the expression for the specific argument.

    This helper should only be used with non-star arguments.
    """
    if name not in ctx.callee_arg_names:
        return None
    idx = ctx.callee_arg_names.index(name)
    args = ctx.args[idx]
    if len(args) != 1:
        # Either an error or no value passed.
        return None
    return args[0]


def get_argtype_by_name(ctx: FunctionContext, name: str) -> Optional[Type]:
    """Same as above but for argument type."""
    if name not in ctx.callee_arg_names:
        return None
    idx = ctx.callee_arg_names.index(name)
    arg_types = ctx.arg_types[idx]
    if len(arg_types) != 1:
        # Either an error or no value passed.
        return None
    return arg_types[0]


def field_hook(ctx: FunctionContext) -> Type:
    """Infer better types for Field calls.

    Examples:
        Field(str) -> Field[Optional[str]]
        Field(str, primary_key=True) -> Field[str]
        Field(str, noneable=False) -> Field[str]
        Column(str, default=...) -> Field[str]
        Column(str, default=..., noneable=True) -> Field[Optional[str]]

    TODO: check the type of 'default'.
    """
    assert isinstance(ctx.default_return_type, Instance)  # type: ignore[misc]

    noneable_arg = get_argument_by_name(ctx, 'noneable')
    primary_arg = get_argument_by_name(ctx, 'primary_key')
    default_arg = get_argument_by_name(ctx, 'default')
    auto_increment_arg = get_argument_by_name(ctx, 'auto_increment')

    auto_increment = False
    if auto_increment_arg:
        auto_increment = parse_bool(auto_increment_arg)

    if primary_arg:
        noneable = not parse_bool(primary_arg)
    else:
        if noneable_arg:
            noneable = parse_bool(noneable_arg)
        else:
            noneable = False
    # TODO: Add support for literal types.

    if not noneable:
        if auto_increment or default_arg:
            set_not_required_field(ctx.default_return_type)
        return ctx.default_return_type
    assert len(ctx.default_return_type.args) == 1
    arg_type = ctx.default_return_type.args[0]
    args: List[Type] = [UnionType([arg_type, NoneTyp()])]
    f = Instance(ctx.default_return_type.type, args,
                 line=ctx.default_return_type.line,
                 column=ctx.default_return_type.column)
    if auto_increment or noneable or default_arg:
        set_not_required_field(f)
    return f


def set_not_required_field(f: Type) -> None:
    f.args.append(AnyType(1))


def is_required_field(f: Type) -> bool:
    return len(f.args) == 1


# We really need to add this to TypeChecker API
def parse_bool(expr: Expression) -> Optional[bool]:
    if isinstance(expr, NameExpr):
         if expr.fullname == 'builtins.True':
             return True
         if expr.fullname == 'builtins.False':
             return False
    return None


def add_class_method(
        ctx: ClassDefContext,
        name: str,
        args: List[Argument],
        return_type: Type,
        self_type: Optional[Type] = None,
        tvar_def: Optional[TypeVarDef] = None,
) -> None:
    """Adds a new class method to a class.
    """
    info = ctx.cls.info

    # First remove any previously generated methods with the same name
    # to avoid clashes and problems in the semantic analyzer.
    if name in info.names:
        sym = info.names[name]
        if sym.plugin_generated and isinstance(sym.node, FuncDef):
            ctx.cls.defs.body.remove(sym.node)

    self_type = self_type or fill_typevars(info)
    function_type = ctx.api.named_type('__builtins__.function')

    args = [Argument(Var('_cls'), TypeType.make_normalized(self_type), None, ARG_POS)] + args
    arg_types, arg_names, arg_kinds = [], [], []
    for arg in args:
        assert arg.type_annotation, 'All arguments must be fully typed.'
        arg_types.append(arg.type_annotation)
        arg_names.append(arg.variable.name)
        arg_kinds.append(arg.kind)

    signature = CallableType(arg_types, arg_kinds, arg_names, return_type, function_type)
    if tvar_def:
        signature.variables = [tvar_def]

    func = FuncDef(name, args, Block([PassStmt()]))
    func.info = info
    func.type = set_callable_name(signature, func)
    func.is_class = True
    func._fullname = info.fullname + '.' + name
    func.line = info.line

    # NOTE: we would like the plugin generated node to dominate, but we still
    # need to keep any existing definitions so they get semantically analyzed.
    if name in info.names:
        # Get a nice unique name instead.
        r_name = get_unique_redefinition_name(name, info.names)
        info.names[r_name] = info.names[name]

    func.is_decorated = True
    v = Var(name, func.type)
    v.info = info
    v._fullname = func._fullname
    v.is_classmethod = True
    dec = Decorator(func, [NameExpr('classmethod')], v)

    dec.line = info.line
    sym = SymbolTableNode(MDEF, dec)

    sym.plugin_generated = True

    info.names[name] = sym
    info.defn.defs.body.append(func)


def plugin(version: str) -> 'TypingType[Plugin]':
    return BasicOLOPlugin
