from typing import Any, Callable

from olo.database import BaseDataBase
from olo.libs.pool import Pool


class PostgreSQLDataBase(BaseDataBase):
    pool: Pool

    def __init__(self, host: str, port: int, user: str, password: str, dbname: str,
                 charset: str = ...,
                 beansdb: Any = ..., autocommit: bool = ...,
                 report: Callable[..., None] = ...,
                 pool_size: int = ...,
                 pool_timeout: int = ...,
                 pool_recycle: int = ...,
                 pool_max_overflow: int = ...) -> None: ...
