from typing import Any, Callable

from olo.transaction import Transaction


class BaseDataBase:
    def __init__(self, beansdb: Any = ..., autocommit: bool = ...,
                 report: Callable[..., None] = ...) -> None: ...

    def transaction(self) -> Transaction: ...


class DataBase(BaseDataBase):
    def __init__(self, store: Any, beansdb: Any = ..., autocommit: bool = ...,
                 report: Callable[..., None] = ...) -> None: ...
