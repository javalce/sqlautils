import re
from typing import Any, Dict, Union

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


def camel_to_snake_case(name: str) -> str:
    name = re.sub(r"((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))", r"_\1", name)
    return name.lower().lstrip("_")


class Tablename:
    def __get__(self, _: Any, cls: Any) -> Any:
        if cls.__dict__.get("__tablename__") is None and cls.__dict__.get("__table__") is None:
            cls.__tablename__ = camel_to_snake_case(cls.__name__)
        return getattr(cls, "__tablename__", None)


class ModelMixin:
    __metadatas__: Dict[Union[str, None], Any] = {}
    __tablename__: Any = Tablename()

    def __init_subclass__(cls, **kwargs: Any) -> None:
        bind_key = getattr(cls, "__bind_key__", None)
        if bind_key is not None:
            if bind_key not in cls.__metadatas__:
                cls.__metadatas__[bind_key] = MetaData()
            cls.metadata = cls.__metadatas__[bind_key]  # type: ignore
        elif None not in cls.__metadatas__ and getattr(cls, "metadata", None) is not None:
            cls.__metadatas__[None] = cls.metadata  # type: ignore
        super().__init_subclass__(**kwargs)


class BaseModel(ModelMixin, DeclarativeBase):
    """The base model class.

    This class is a subclass of the SQLAlchemy `DeclarativeBase` class and is
    intended to be used as the base class for all models in the application.
    """

    __abstract__ = True
