from typing import TypeVar, Generic

T = TypeVar('T')

class Interface: ...

class SQLASTInterface(Interface, Generic[T]):
    alias_name: str
