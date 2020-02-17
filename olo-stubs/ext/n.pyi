from typing import TypeVar, Callable

T = TypeVar('T')

def n(default: Callable[..., T]) -> Callable[..., T]: ...
