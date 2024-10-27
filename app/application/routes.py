from flask import Blueprint, current_app
from .data_access.repository import ApplicationRepo

application_bp = Blueprint("application", __name__)


@application_bp.route("/all", methods=["GET"])
def profile():
    db = current_app.extensions["sqlalchemy"].db

    application_repo = ApplicationRepo(session=db.session)

    # Fetch all applications
    applications = application_repo.list()

    # Return the applications as a JSON response
    return {"applications": [application.to_dict() for application in applications]}
