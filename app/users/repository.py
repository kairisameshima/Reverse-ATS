from typing import Optional
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Session

from app.db import User as UserTable
from app.lib.data_access.interface import RepositoryInterface
from app.users.domain_models import MutableUserFields, User


class UserRepository(RepositoryInterface[User]):
    def __init__(self, session: Session):
        self.session = session

    def get(self, uuid: UUID) -> User:
        users = self.list(uuids=[uuid])
        if not users:
            raise ValueError(f"User with ID {uuid} not found")
        return users[0]

    def list(self, uuids: Optional[list[UUID]] = None) -> list[User]:
        query = sa.select(UserTable)
        if uuids:
            query = query.filter(UserTable.uuid.in_(uuids))
        rows = self.session.execute(query).scalars().all()
        entities = [self._from_row(row) for row in rows]

        return entities

    def add(self, entity: User) -> UUID:
        user = UserTable(
            uuid=entity.uuid,
            google_user_id=entity.google_user_id,
            name=entity.name,
            email=entity.email,
            image_url=entity.image_url,
        )
        self.session.add(user)
        self.session.flush()
        return entity.uuid

    def update(self, uuid: UUID, **kwargs) -> None:
        kwargs = self._filter_mutable_fields(kwargs)
        self.session.execute(
            sa.update(UserTable).where(UserTable.uuid == uuid).values(**kwargs)
        )

    def delete(self, uuid: UUID) -> None:
        self.session.execute(
            sa.delete(UserTable).where(UserTable.uuid == uuid)
        )

    @staticmethod
    def _from_row(row: sa.engine.Row) -> User:
        return User(
            uuid=row.uuid,
            google_user_id=row.google_user_id,
            name=row.name,
            email=row.email,
            image_url=row.image_url,
        )

    @staticmethod
    def _filter_mutable_fields(kwargs: dict) -> dict:
        mutable_fields = {
            field for field in MutableUserFields.__annotations__.keys()}
        return {
            k: v for k, v in kwargs.items() if k in mutable_fields and v is not None
        }
