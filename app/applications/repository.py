from typing import Optional
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Session

from app.applications.domain_models import Application, MutableApplicationFields
from app.db import Application as ApplicationTable
from app.lib.data_access.interface import RepositoryInterface


class ApplicationRepository(RepositoryInterface[Application]):
    def __init__(self, session: Session):
        self.session = session

    def get(self, uuid: UUID) -> Application:
        Applications = self.list(uuids=[uuid])
        if not Applications:
            raise ValueError(f"Application with ID {uuid} not found")
        return Applications[0]

    def list(self, uuids: Optional[list[UUID]] = None) -> list[Application]:
        query = sa.select(ApplicationTable)
        if uuids:
            query = query.filter(ApplicationTable.uuid.in_(uuids))
        rows = self.session.execute(query).scalars().all()
        entities = [self._from_row(row) for row in rows]

        return entities

    def add(self, entity: Application) -> UUID:
        query = sa.insert(ApplicationTable).values(
            uuid=entity.uuid,
            company=entity.company,
            description=entity.description,
            user_uuid=entity.user_uuid,
            position=entity.position,
            status=entity.status,
            date_applied=entity.date_applied,
            date_first_response=entity.date_first_response,
            date_rejected=entity.date_rejected,
        )
        self.session.execute(query)
        return entity.uuid

    def update(self, uuid: UUID, **kwargs) -> None:
        kwargs = self._filter_mutable_fields(kwargs)
        self.session.execute(
            sa.update(ApplicationTable).where(
                ApplicationTable.uuid == uuid).values(**kwargs)
        )

    def delete(self, uuid: UUID) -> None:
        self.session.execute(
            sa.delete(ApplicationTable).where(ApplicationTable.uuid == uuid)
        )

    @staticmethod
    def _from_row(row: sa.engine.Row) -> Application:
        pass
        return Application(
            uuid=row.uuid,
            company=row.company,
            description=row.description,
            user_uuid=row.user_uuid,
            position=row.position,
            status=row.status,
            date_applied=row.date_applied,
            date_first_response=row.date_first_response,
            date_rejected=row.date_rejected,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    @staticmethod
    def _filter_mutable_fields(kwargs: dict) -> dict:
        mutable_fields = {
            field for field in MutableApplicationFields.__annotations__.keys()}
        return {
            k: v for k, v in kwargs.items() if k in mutable_fields and v is not None
        }
