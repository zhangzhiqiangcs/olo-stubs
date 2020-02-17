from typing import Any, Callable

from olo.transaction import Transaction


class BaseDataBase:
    def __init__(self, beansdb: Any = ..., autocommit: bool = ...,
                 report: Callable[..., None] = ...) -> None: ...

    def transaction(self) -> Transaction: ...

    def create_all(self) -> None: ...

    def execute(self, sql: str, params: Any = ...): ...


class DataBase(BaseDataBase):
    def __init__(self, store: Any, beansdb: Any = ..., autocommit: bool = ...,
                 report: Callable[..., None] = ...) -> None: ...
