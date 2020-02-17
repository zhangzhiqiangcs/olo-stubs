from __future__ import annotations
from typing import TypeVar, Type, Generic, Optional, Callable, Container, Any, overload, Tuple

from .expression import BinaryExpression
from .interfaces import SQLASTInterface
from .olo_types import SQLValue as SQLValue

T = TypeVar('T')
F = TypeVar('F', bound='BaseField')


class BaseField(SQLASTInterface[T], Generic[T]):
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

    @overload
    def __get__(self: F, instance: None, owner: Any) -> F: ...

    @overload
    def __get__(self, instance: object, owner: Any) -> T: ...

    def in_(self: F, other: Container[T]) -> BinaryExpression[F, Container[T]]: ...

    def not_in_(self: F, other: Container[T]) -> BinaryExpression[F, Container[T]]: ...

    def like_(self: F, other: T) -> BinaryExpression[F, T]: ...

    def ilike_(self: F, other: T) -> BinaryExpression[F, T]: ...

    def regexp_(self: F, other: T) -> BinaryExpression[F, T]: ...

    def between_(self: F, other: Tuple) -> BinaryExpression[F, Tuple]: ...

    def concat_(self: F, other: T) -> BinaryExpression[F, T]: ...

    def is_(self: F, other: T) -> BinaryExpression[F, T]: ...

    def is_not_(self: F, other: T) -> BinaryExpression[F, T]: ...

    def __add__(self: F, other: T) -> BinaryExpression[F, T]: ...
    def __radd__(self: F, other: T) -> BinaryExpression[F, T]: ...
    def __sub__(self: F, other: T) -> BinaryExpression[F, T]: ...
    def __rsub__(self: F, other: T) -> BinaryExpression[F, T]: ...
    def __mul__(self: F, other: T) -> BinaryExpression[F, T]: ...
    def __div__(self: F, other: T) -> BinaryExpression[F, T]: ...
    def __truediv__(self: F, other: T) -> BinaryExpression[F, T]: ...
    def __mod__(self: F, other: T) -> BinaryExpression[F, T]: ...
    def __eq__(self: F, other: T) -> BinaryExpression[F, T]: ... # type: ignore[override]
    def __ne__(self: F, other: T) -> BinaryExpression[F, T]: ... # type: ignore[override]
    def __gt__(self: F, other: T) -> BinaryExpression[F, T]: ... # type: ignore[override]
    def __ge__(self: F, other: T) -> BinaryExpression[F, T]: ... # type: ignore[override]
    def __lt__(self: F, other: T) -> BinaryExpression[F, T]: ... # type: ignore[override]
    def __le__(self: F, other: T) -> BinaryExpression[F, T]: ... # type: ignore[override]
    def __lshift__(self: F, other: T) -> BinaryExpression[F, T]: ...


class Field(BaseField[T]): ...
