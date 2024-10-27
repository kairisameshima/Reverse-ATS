from app.application.domain_models import Application
from app.application.data_access.repository import ApplicationRepo
import pytest

from app.lib.exceptions import RecordNotFoundError


@pytest.fixture
def application_repo(session):
    return ApplicationRepo(session=session)


def test_add_application(application_repo, session):
    # Test adding a new application with fields
    note = "This is a test note."
    application = Application(note=note)
    application_uuid = application_repo.add(application=application)

    assert application.uuid == application_uuid


def test_get_application_by_uuid(application_repo, session):
    note = "Test application retrieval."
    application_uuid = application_repo.add(Application(note=note))
    retrieved_application = application_repo.get(application_uuid)

    assert retrieved_application is not None
    assert retrieved_application.uuid == application_uuid
    assert retrieved_application.note == note


def test_update_application(application_repo, session):
    note = "Initial note."
    new_note = "Updated note."
    application_uuid = application_repo.add(Application(note=note))
    application_repo.update(uuid=application_uuid, note=new_note)
    updated_application = application_repo.get(uuid=application_uuid)

    assert updated_application is not None
    assert updated_application.note == new_note


def test_delete_application(application_repo, session):
    note = "Application to delete."
    application_uuid = application_repo.add(Application(note=note))
    application_repo.delete(uuid=application_uuid)

    with pytest.raises(RecordNotFoundError):
        _ = application_repo.get(uuid=application_uuid)
