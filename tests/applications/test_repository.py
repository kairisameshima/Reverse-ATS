from uuid import uuid4

import sqlalchemy as sa

from app.applications.domain_models import Application as ApplicationModel
from app.applications.repository import ApplicationRepository
from app.db import Application as ApplicationTable
from app.db import User as UserTable


def test_get_applications(db_session):
    # Arrange
    repository = ApplicationRepository(session=db_session)
    user_1 = UserTable(
        name="user_1",
        email="test@mail.com",
        image_url="image_url",
    )
    db_session.add(user_1)
    db_session.commit()

    app_1 = ApplicationTable(
        name="app_1",
        description="app_1",
        position="app_1",
        user_uuid=user_1.uuid,
    )

    db_session.add(app_1)
    db_session.commit()

    # Act
    apps = repository.list()

    # Assert
    assert len(apps) == 1


def test_create_application(db_session):
    # Arrange
    repository = ApplicationRepository(session=db_session)
    user_1 = UserTable(
        name="user_1",
        email="test@mail.com",
        image_url="image_url",
    )
    db_session.add(user_1)
    db_session.commit()

    app = ApplicationModel(
        name="app_1",
        description="app_1",
        user_uuid=user_1.uuid,
        position="app_1",
    )

    # Act
    app_uuid = repository.add(app)
    db_session.commit()

    query = sa.select(ApplicationTable).where(ApplicationTable.uuid == app_uuid)
    row = db_session.execute(query).scalars().first()

    # Assert
    assert app_uuid is not None
    assert row is not None


def test_update_application(db_session):
    # Arrange
    repository = ApplicationRepository(session=db_session)
    user_1 = UserTable(
        name="user_1",
        email="test@mail.com",
        image_url="image_url",
    )
    db_session.add(user_1)
    db_session.commit()

    app = ApplicationModel(
        name="app_1",
        description="app_1",
        user_uuid=user_1.uuid,
        position="app_1",
    )
    app_uuid = repository.add(app)
    db_session.commit()

    # Act
    repository.update(app_uuid, name="app_2")
    db_session.commit()

    # Assert
    query = sa.select(ApplicationTable).where(ApplicationTable.uuid == app_uuid)
    row = db_session.execute(query).scalars().first()
    assert row.name == "app_2"
