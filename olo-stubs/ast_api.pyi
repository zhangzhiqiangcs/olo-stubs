from typing import Generator, TypeVar, overload, Union, Tuple

from olo.field import Field
from olo.funcs import Function
from olo.query import Query

T = TypeVar('T')
T0 = TypeVar('T0')
T1 = TypeVar('T1')
T2 = TypeVar('T2')

U = TypeVar('U')

F = Union[Field[T], Function[T]]

TU2 = Union[
    Tuple[T, F[T0]],
    Tuple[F[T], T0],
    Tuple[F[T], F[T0]],
]

TU3 = Union[
    Tuple[T, T0, F[T1]],
    Tuple[T, F[T0], T1],
    Tuple[F[T], T0, T1],
    Tuple[T, F[T0], F[T1]],
    Tuple[F[T], F[T0], T1],
    Tuple[F[T], T0, F[T1]],
    Tuple[F[T], F[T0], F[T1]],
]

TU4 = Union[
    Tuple[T, T0, T1, F[T2]],
    Tuple[T, T0, F[T1], T2],
    Tuple[T, F[T0], T1, T2],
    Tuple[F[T], T0, T1, T2],
    Tuple[T, T0, F[T1], F[T2]],
    Tuple[T, F[T0], F[T1], T2],
    Tuple[F[T], F[T0], T1, T2],
    Tuple[F[T], T0, T1, F[T2]],
    Tuple[T, F[T0], F[T1], F[T2]],
    Tuple[F[T], F[T0], F[T1], T2],
    Tuple[F[T], F[T0], T1, F[T2]],
    Tuple[F[T], T0, F[T1], F[T2]],
    Tuple[F[T], F[T0], F[T1], F[T2]],
]

@overload
def select(g: Generator[TU4[T, T0, T1, T2], U, U]) -> Query[Tuple[T, T0, T1, T2]]: ...

@overload
def select(g: Generator[TU3[T, T0, T1], U, U]) -> Query[Tuple[T, T0, T1]]: ...

@overload
def select(g: Generator[TU2[T, T0], U, U]) -> Query[Tuple[T, T0]]: ...

@overload
def select(g: Generator[Tuple[F[T]], U, U]) -> Query[T]: ...

@overload
def select(g: Generator[F[T], U, U]) -> Query[T]: ...

@overload
def select(g: Generator[T, U, U]) -> Query[T]: ...