from typing import TypeVar, Callable, overload

T = TypeVar('T')

@overload
def n(default: Callable[..., T]) -> Callable[..., T]: ...

@overload
def n(default: T) -> Callable[..., T]: ...
