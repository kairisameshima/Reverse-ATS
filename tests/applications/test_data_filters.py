from app.applications.data_filters import ApplicationDataFilters
from app.db import Application as ApplicationTable
from app.db import User as UserTable


def test_get_application_uuids_by_user(db_session):
    # Arrange
    # Create a user
    user_1 = UserTable(
        name="user_1",
        email="mail.com",
        image_url="image_url",
    )
    user_2 = UserTable(
        name="user_2",
        email="mail2.com",
        image_url="image_url",
    )

    db_session.add_all([user_1, user_2])
    db_session.commit()

    # Create applications for the users
    app_1 = ApplicationTable(
        name="app_1",
        description="app_1",
        position="app_1",
        user_uuid=user_1.uuid,
    )
    app_2 = ApplicationTable(
        name="app_2",
        description="app_2",
        position="app_2",
        user_uuid=user_1.uuid,
    )
    app_3 = ApplicationTable(
        name="app_3",
        description="app_3",
        position="app_3",
        user_uuid=user_2.uuid,
    )

    db_session.add_all([app_1, app_2, app_3])
    db_session.commit()

    # Get the application uuids for user_1
    filters = ApplicationDataFilters(session=db_session)

    # Act
    uuids = filters.get_application_uuids_for_user(user_uuid=user_1.uuid)

    # Assert
    assert len(uuids) == 2
    assert app_1.uuid in uuids
    assert app_2.uuid in uuids
