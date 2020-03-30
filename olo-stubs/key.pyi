from typing import Any


class Key(tuple):
    def get_hashed_value(self) -> Any: ...


class StrKey(Key): ...
