from typing import Any, Callable

from olo.database import BaseDataBase


class MySQLDataBase(BaseDataBase):

    def __init__(self, host: str, port: int, user: str, password: str, dbname: str,
                 charset: str = ...,
                 beansdb: Any = ..., autocommit: bool = ...,
                 report: Callable[..., None] = ...,
                 max_active_size: int = ...,
                 max_idle_size: int = ...) -> None: ...
