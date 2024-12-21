request_data = {'company': 'tfwtfw', 'position': 'fwtft', 'status': 'prospect', 'dateApplied': '2024-12-20'}

from app.applications.data_models import ApplicationCreateRequest


def test_application_create_request():
    application_data = ApplicationCreateRequest(
        **request_data
    )
