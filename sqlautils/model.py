from sqlalchemy.orm import DeclarativeBase, declared_attr


class BaseModel(DeclarativeBase):
    """The base model class.

    This class is a subclass of the SQLAlchemy `DeclarativeBase` class and is
    intended to be used as the base class for all models in the application.
    """

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
