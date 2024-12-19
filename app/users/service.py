from logging import Logger
from uuid import UUID

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.users.data_filters import UserDataFilters
from app.users.data_models import UserFromEndPoint
from app.users.domain_models import User
from app.users.repository import UserRepository

logger = Logger(__name__)


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def get_or_create_user_from_google(self, user_data: UserFromEndPoint) -> UUID:
        """Get or create a user from the database."""
        user_repo = UserRepository(self.session)
        user_data_filters = UserDataFilters(self.session)

        try:
            return user_data_filters.get_by_google_user_id(user_data.google_user_id)
        except NoResultFound:
            return user_repo.add(User(**user_data.model_dump()))
