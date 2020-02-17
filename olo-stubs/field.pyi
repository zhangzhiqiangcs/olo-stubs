from __future__ import annotations

from typing import TypeVar, Type, Generic, Optional, Callable, Container, Any, overload

from .interfaces import SQLASTInterface
from .olo_types import SQLValue as SQLValue
from .operations import BinaryOperationMixin, UnaryOperationMixin

T = TypeVar('T')
F = TypeVar('F', bound='BaseField')


class BaseField(SQLASTInterface[T], UnaryOperationMixin, BinaryOperationMixin[T], Generic[T]):
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


class Field(BaseField[T]): ...
