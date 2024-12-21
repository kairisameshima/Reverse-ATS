from typing import Optional, Protocol, TypeVar
from uuid import UUID

from app.lib.data_access.domain_model import DomainModel

T = TypeVar("T", bound=DomainModel)  # A domain model type


class RepositoryInterface(Protocol[T]):
    def get(self, uuid: UUID) -> T:
        """Get a domain model instance by its canonical unique ID."""
        ...

    def list(self, uuids: Optional[list[UUID]] = None) -> list[T]:
        """
        Get a list of domain model instances.
        A list of UUIDs can be provided to filter the results.
        """
        ...

    def add(self, entity: T) -> UUID:
        """Add a new domain model instance and return its UUID."""
        ...

    def update(self, uuid: UUID, **kwargs) -> None:
        """
        Update a domain model instance.
        The UUID is required to identify the instance.
        """
        ...

    def delete(self, uuid: UUID) -> None:
        """Delete a domain model instance."""
        ...
