from typing import TypeVar, Generic

T = TypeVar('T')
L = TypeVar('L')
R = TypeVar('R')

class UnaryExpression(Generic[T]):
    ...


class BinaryExpression(Generic[L, R]):
    ...
