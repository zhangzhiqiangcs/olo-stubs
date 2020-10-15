from __future__ import annotations

from typing import TypeVar, Type, Generic, Optional, Callable, Container, Any, overload, Tuple, List

from .interfaces import SQLASTInterface
from .olo_types import SQLValue as SQLValue
from .mixins.operations import BinaryOperationMixin, UnaryOperationMixin
from .types.json import JSONLike

T = TypeVar('T')
U = TypeVar('U')
F = TypeVar('F', bound='BaseField')
BF = TypeVar('BF', bound='BatchField')


class BaseField(Generic[T]):
    type: Type[T]
    default: Optional[T]
    name: str
    _parser: Optional[Callable[..., T]]
    _deparser: Optional[Callable[[T], SQLValue]]
    _primary_key: bool
    on_update: Optional[Callable[..., T]]
    choices: Optional[Container[T]]
    encrypt: bool
    input: Optional[Callable[[T], T]]
    output: Optional[Callable[[T], T]]
    noneable: bool
    attr_name: str
    version: Optional[str]
    length: Optional[int]
    auto_increment: bool
    charset: Optional[str]
    AES_KEY: str

    def __init__(self, type_: Type[T],
                 default: Optional[T] = ...,
                 name: Optional[str] = ...,
                 parser: Optional[Callable[..., T]] = ...,
                 deparser: Optional[Callable[[T], SQLValue]] = ...,
                 primary_key: bool = ...,
                 on_update: Optional[Callable[..., T]] = ...,
                 choices: Optional[Container[T]] = ...,
                 encrypt: bool = ...,
                 input: Optional[Callable[[T], T]] = ...,
                 output: Optional[Callable[[T], T]] = ...,
                 noneable: bool = ...,
                 attr_name: Optional[str] = ...,
                 version: Optional[str] = ...,
                 length: Optional[int] = ...,
                 auto_increment: bool = ...,
                 charset: Optional[str] = ...) -> None: ...

    @property
    def table_name(self) -> Optional[str]: ...

    def get_default(self) -> Optional[T]: ...

    def parse(self, value: Any) -> T: ...

    def deparse(self, value: T) -> SQLValue: ...

    def getter(self: F, func: Callable[[Any, T], T]) -> F: ...

    def setter(self: F, func: Callable[[Any, T], T]) -> F: ...

    @overload
    def __get__(self: F, instance: None, owner: Any) -> F: ...

    @overload
    def __get__(self, instance: object, owner: Any) -> T: ...


class Field(BaseField[T], UnaryOperationMixin, BinaryOperationMixin[T], SQLASTInterface[T], Generic[T]): ...


class ConstField(Field[T], Generic[T]):
    value: T

    def __init__(self, value: T) -> None: ...

    @overload
    def __get__(self: F, instance: None, owner: Any) -> F: ...

    @overload
    def __get__(self, instance: object, owner: Any) -> T: ...


class UnionField(BaseField, UnaryOperationMixin, BinaryOperationMixin, SQLASTInterface, Generic[F]):
    fields: Tuple[Any]

    def __init__(self, *fields: Any) -> None: ...


class JSONField(Field[JSONLike]):
    def __init__(self,
                 default: Optional[JSONLike] = ...,
                 name: Optional[str] = ...,
                 parser: Optional[Callable[..., JSONLike]] = ...,
                 deparser: Optional[Callable[[JSONLike], SQLValue]] = ...,
                 primary_key: bool = ...,
                 on_update: Optional[Callable[..., JSONLike]] = ...,
                 choices: Optional[Container[JSONLike]] = ...,
                 encrypt: bool = ...,
                 input: Optional[Callable[[JSONLike], JSONLike]] = ...,
                 output: Optional[Callable[[JSONLike], JSONLike]] = ...,
                 noneable: bool = ...,
                 attr_name: Optional[str] = ...,
                 version: Optional[str] = ...,
                 length: Optional[int] = ...,
                 auto_increment: bool = ...,
                 charset: Optional[str] = ...) -> None: ...


class DbField(BaseField): ...


class BatchField(Generic[T]):
    @overload
    def __init__(self, type_: Type[T],
                 default: Optional[T] = ...,
                 name: Optional[str] = ...) -> None: ...

    @overload
    def __init__(self, type_: Callable[..., Type[T]],
                 default: Optional[T] = ...,
                 name: Optional[str] = ...) -> None: ...

    def getter(self, func: Callable[[Type[U], List[U]], List[Optional[T]]]) -> Callable[[Type[U], List[U]], List[Optional[T]]]: ...

    @overload
    def __get__(self: BF, instance: None, owner: Any) -> BF: ...

    @overload
    def __get__(self, instance: object, owner: Any) -> Optional[T]: ...
