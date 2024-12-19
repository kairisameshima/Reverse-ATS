from uuid import UUID

from app.users.data_models import UserFromEndPoint
from app.users.domain_models import User
from app.users.repository import UserRepository
from app.users.service import UserService


def test_get_or_create_user(db_session):
    # Arrange
    user_data = UserFromEndPoint(
        google_user_id="123",
        email="hi@mail.com",
        name="John Doe",
        image_url="https://example.com/image.jpg",
    )
    user_service = UserService(db_session)

    # Act
    user_id = user_service.get_or_create_user_from_google(user_data)

    # Assert
    assert user_id is not None
    assert isinstance(user_id, UUID)


def test_get_or_create_user_already_exists(db_session):
    # Arrange
    existing_user = User(
        google_user_id="123",
        email="mail.com",
        name="John Doe",
        image_url="https://example.com/image.jpg",
    )
    user_data = UserFromEndPoint(
        google_user_id="123",
        email="mail.com",
        name="John Doe",
        image_url="https://example.com/image.jpg",
    )

    user_service = UserService(db_session)
    user_repository = UserRepository(db_session)
    existing_uuid = user_repository.add(existing_user)

    db_session.commit()

    # Act
    user_id = user_service.get_or_create_user_from_google(user_data)

    # Assert
    assert user_id == existing_uuid
