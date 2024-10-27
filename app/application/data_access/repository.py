from db.tables.application import Application as ApplicationTable  # Import the model
from ..domain_models import Application
import sqlalchemy as sa
from typing import Optional
from uuid import UUID
from app.lib.exceptions import RecordNotFoundError


class ApplicationRepo:
    def __init__(self, session):
        self.session = session

    def get(self, uuid: UUID) -> Application:
        """Fetch an application by its UUID."""
        application = self.session.query(ApplicationTable).filter_by(uuid=uuid).first()
        if not application:
            raise RecordNotFoundError(uuid, ApplicationTable)
        return self._model_from_row(application)

    def list(self, uuids: Optional[list[UUID]] = None) -> list[Application]:
        """Fetch all applications."""
        return [
            self._model_from_row(application)
            for application in self.session.query(ApplicationTable).all()
        ]

    def add(self, application: Application) -> UUID:
        """Add a new application with the given note."""
        new_record = ApplicationTable(
            uuid=application.uuid,
            note=application.note,
        )
        self.session.add(new_record)
        self.session.commit()
        return application.uuid

    def update(self, uuid, **kwargs):
        """Update fields of an existing application based on keyword arguments."""
        application = self.session.query(ApplicationTable).filter_by(uuid=uuid).first()
        if application:
            # Update only the fields that are provided in kwargs
            for key, value in kwargs.items():
                if hasattr(application, key):
                    setattr(application, key, value)
            self.session.commit()
        return application

    def delete(self, uuid):
        """Delete an application by its UUID."""
        application = self.session.query(ApplicationTable).filter_by(uuid=uuid).first()
        if application:
            self.session.delete(application)
            self.session.commit()
        return application

    @staticmethod
    def _model_from_row(row: sa.engine.Row) -> Application:
        return Application(
            uuid=row.uuid,
            note=row.note,
            create_date=row.create_date,
            update_date=row.update_date,
        )
