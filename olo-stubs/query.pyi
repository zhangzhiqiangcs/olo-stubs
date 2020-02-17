from typing import TypeVar, Generic, Any, overload, List, Tuple, Optional, Generator, Union

from .expression import BinaryExpression, UnaryExpression
from .field import Field
from .funcs import Function, COUNT, SUM, AVG, LENGTH, MAX, MIN, PartialIf
from .model import Model

T = TypeVar('T')
T0 = TypeVar('T0')
T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
T5 = TypeVar('T5')
T6 = TypeVar('T6')
F = Union[
    Field[T],
    Function[T],
    BinaryExpression[Field[T], T],
    BinaryExpression[Function[T], T],
    BinaryExpression[PartialIf[T], T],
]
M = TypeVar('M', bound=Model)
Q = TypeVar('Q', bound='Query')


class Query(Generic[T]):
    def filter(self: Q, *expressions: BinaryExpression, **expression_dict: Any) -> Q: ...
    @overload
    def map(self, entity: M) -> Query[M]: ...
    @overload
    def map(self, entity0: F[T0]) -> Query[T0]: ...
    @overload
    def map(self, entity0: F[T0], entity1: F[T1]) -> Query[Tuple[T0, T1]]: ...
    @overload
    def map(self, entity0: F[T0], entity1: F[T1], entity: F[T2]) -> Query[Tuple[T0, T1, T2]]: ...
    @overload
    def map(self, entity0: F[T0], entity1: F[T1], entity2: F[T2], entity3: F[T3]) -> Query[Tuple[T0, T1, T2, T3]]: ...
    @overload
    def map(self, *entities: Any): ...
    @overload
    def __call__(self, entity: M) -> Query[M]: ...
    @overload
    def __call__(self, entity0: F[T0]) -> Query[T0]: ...
    @overload
    def __call__(self, entity0: F[T0], entity1: F[T1]) -> Query[Tuple[T0, T1]]: ...
    @overload
    def __call__(self, entity0: F[T0], entity1: F[T1], entity: F[T2]) -> Query[Tuple[T0, T1, T2]]: ...
    @overload
    def __call__(self, entity0: F[T0], entity1: F[T1], entity2: F[T2], entity3: F[T3]) -> Query[Tuple[T0, T1, T2, T3]]: ...
    @overload
    def __call__(self, *entities: Any): ...
    @overload
    def __getitem__(self, item: int) -> Optional[T]: ...
    @overload
    def __getitem__(self, item: slice) -> List[T]: ...
    def __iter__(self: Query[T]) -> Generator[T, T0, T0]: ...
    def all(self) -> List[T]: ...
    def first(self) -> Optional[T]: ...
    def limit(self: Q, limit: int) -> Q: ...
    def offset(self: Q, offset: int) -> Q: ...
    def order_by(self: Q, *criterion: UnaryExpression) -> Q: ...
    def group_by(self: Q, *criterion: Field) -> Q: ...
    def having(self: Q, *expressions: BinaryExpression, **expression_dict: Any) -> Q: ...
    def on(self: Q, *expressions: BinaryExpression, **expression_dict: Any) -> Q: ...
    def for_update(self: Q) -> Q: ...
    def count(self) -> int: ...
    def count_and_all(self) -> Tuple[int, List[T]]: ...
    def update(self: Q, **values: Any) -> Optional[T]: ...
    def delete(self: Q) -> Optional[T]: ...
