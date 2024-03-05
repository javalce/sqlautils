from typing import Generic, List, Type, TypeVar, Union

from sqlalchemy import select
from sqlalchemy.orm import Session

from .model import BaseModel
from .session import get_session

T = TypeVar("T", bound=BaseModel)
K = TypeVar("K")


class BaseRepository(Generic[T, K]):
    """Base class for all repositories. It provides basic CRUD operations."""

    model_class: Type[T]

    @property
    def session(self) -> Session:
        """Returns the current session."""
        return get_session()

    def find_all(self) -> List[T]:
        """Returns all instances of the model."""
        query = select(self.model_class)

        return list(self.session.scalars(query).all())

    def find_by_id(self, id: K) -> Union[T, None]:
        """Returns an instance of the model by its id. If not found, returns None."""
        return self.session.get(self.model_class, id)

    def save(self, instance: T) -> T:
        """Saves an instance of the model."""
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def save_all(self, instances: List[T]) -> List[T]:
        """Saves a list of instances of the model."""
        self.session.add_all(instances)
        self.session.commit()
        for instance in instances:
            self.session.refresh(instance)
        return instances

    def delete(self, instance: T) -> None:
        """Deletes an instance of the model."""
        self.session.delete(instance)
        self.session.commit()

    def delete_by_id(self, id: K) -> None:
        """Deletes an instance of the model by its id."""
        instance = self.session.get(self.model_class, id)

        if instance:
            self.session.delete(instance)
            self.session.commit()
