from db.tables.application import Application  # Import the model
from app import db


class ApplicationRepo:
    @staticmethod
    def get_application_by_uuid(uuid):
        """Fetch an application by its UUID."""
        return db.session.query(Application).filter_by(uuid=uuid).first()

    @staticmethod
    def add_application(application: Application):
        """Add a new application with the given note."""
        db.session.add(application)
        db.session.commit()
        return application

    @staticmethod
    def update_application(uuid, **kwargs):
        """Update fields of an existing application based on keyword arguments."""
        application = db.session.query(Application).filter_by(uuid=uuid).first()
        if application:
            # Update only the fields that are provided in kwargs
            for key, value in kwargs.items():
                if hasattr(application, key):
                    setattr(application, key, value)
            db.session.commit()
        return application

    @staticmethod
    def delete_application(uuid):
        """Delete an application by its UUID."""
        application = db.session.query(Application).filter_by(uuid=uuid).first()
        if application:
            db.session.delete(application)
            db.session.commit()
        return application
