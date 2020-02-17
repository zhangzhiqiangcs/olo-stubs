from typing import TypeVar, Type, Any, Optional, List, ClassVar, Generator, Dict

from .expression import BinaryExpression
from .query import Query

T = TypeVar('T')
U = TypeVar('U')
M = TypeVar('M', bound='Model')


class ModelMeta(type):
    @property
    def query(cls: Type[T]) -> Query[T]: ...

    def __iter__(cls: Type[T]) -> Generator[T, U, U]: ...


class Model(metaclass=ModelMeta):

    AES_KEY: ClassVar[str]
    __table_name__: str

    def __init__(self, **kwargs: Any) -> None: ...

    @classmethod
    def get(cls: Type[M], ident: Any, *kwargs: Any) -> Optional[M]: ...

    @classmethod
    def get_multi(cls: Type[M], idents: List[T], filter_none: bool = False) -> List[Optional[M]]: ...

    @classmethod
    def gets(cls: Type[M], idents: List[T], filter_none: bool = False) -> List[Optional[M]]: ...

    @classmethod
    def get_by(cls: Type[M], *expressions: BinaryExpression, **expression_dict: Any) -> Optional[M]: ...

    @classmethod
    def get_multi_by(cls: Type[M], *expressions: BinaryExpression, **expression_dict: Any) -> List[M]: ...

    @classmethod
    def gets_by(cls: Type[M], *expressions: BinaryExpression, **expression_dict: Any) -> List[M]: ...

    @classmethod
    def create(cls: Type[M], **kwargs: Any) -> M: ...

    def update(self, **kwargs: Any) -> bool: ...

    def delete(self, **kwargs: Any) -> bool: ...

    def save(self) -> bool: ...

    def to_json(self) -> Dict: ...

    def to_dict(self, excludes=None, parsers=None,
                type_parsers=None, jsonize=False) -> Dict: ...
