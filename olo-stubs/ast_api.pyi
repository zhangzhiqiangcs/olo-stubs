from typing import Generator, TypeVar

from olo.query import Query

T = TypeVar('T')
U = TypeVar('U')


def select(g: Generator[T, U, U]) -> Query[T]: ...