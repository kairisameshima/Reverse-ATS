from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Session

from app.db import Application as ApplicationTable


class ApplicationDataFilters():
    def __init__(self, session: Session):
        self.session = session

    def get_application_uuids_for_user(self, user_uuid: UUID) -> list[UUID]:
        query = sa.select(ApplicationTable.uuid).where(
            ApplicationTable.user_uuid == user_uuid)
        rows = self.session.execute(query).scalars().all()
        return rows
