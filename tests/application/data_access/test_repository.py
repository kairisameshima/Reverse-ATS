from db.tables.application import Application
from app.application.data_access.repository import ApplicationRepo
from app import db


def test_add_application_with_fields(session):
    # Test adding a new application with fields
    note = "This is a test note."

    application = ApplicationRepo.add_application(Application(note=note))

    assert application.note == note
    assert application.uuid is not None


def test_add_application_with_instance(session):
    # Test adding a new application by passing an Application instance
    application_instance = Application(note="Instance test note")
    application = ApplicationRepo.add_application(application=application_instance)

    assert application.note == "Instance test note"
    assert application.uuid is not None


def test_get_application_by_uuid(session):
    note = "Test application retrieval."
    application = ApplicationRepo.add_application(Application(note=note))
    retrieved_application = ApplicationRepo.get_application_by_uuid(application.uuid)

    assert retrieved_application is not None
    assert retrieved_application.uuid == application.uuid
    assert retrieved_application.note == note


def test_update_application(session):
    note = "Initial note."
    new_note = "Updated note."
    application = ApplicationRepo.add_application(Application(note=note))
    ApplicationRepo.update_application(application.uuid, note=new_note)
    updated_application = ApplicationRepo.get_application_by_uuid(application.uuid)

    assert updated_application is not None
    assert updated_application.note == new_note


def test_delete_application(session):
    note = "Application to delete."
    application = ApplicationRepo.add_application(Application(note=note))
    ApplicationRepo.delete_application(application.uuid)
    deleted_application = ApplicationRepo.get_application_by_uuid(application.uuid)

    assert deleted_application is None
