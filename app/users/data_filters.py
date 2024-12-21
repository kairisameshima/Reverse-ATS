from sqlalchemy.orm import Session
from app.db import User as UserTable
from uuid import UUID
import sqlalchemy as sa


class UserDataFilters():
    def __init__(self, session: Session):
        self.session = session

    def get_by_google_user_id(self, google_user_id: str) -> UUID:
        query = sa.select(UserTable.uuid).where(
            UserTable.google_user_id == google_user_id)

        return self.session.execute(query).scalars().one()
