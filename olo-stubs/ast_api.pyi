from typing import Generator, TypeVar, overload, Union, Tuple

from olo.query import Query, F

T = TypeVar('T')
T0 = TypeVar('T0')
T1 = TypeVar('T1')
T2 = TypeVar('T2')

U = TypeVar('U')

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
def select(g: Generator[F[T], U, U]) -> Query[T]: ...

@overload
def select(g: Generator[T, U, U]) -> Query[T]: ...