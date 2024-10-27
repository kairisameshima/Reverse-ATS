import pytest
from app import create_app, db
from flask_migrate import upgrade
from db.tables.application import Application  # Import any models to create the tables


@pytest.fixture(scope="session")
def app():
    """Create and configure a new app instance for each session."""
    app = create_app(testing=True)  # Use the test configuration
    with app.app_context():
        db.create_all()  # Recreate all tables
        yield app
        db.drop_all()  # Drop tables after the session ends


@pytest.fixture(scope="function")
def client(app):
    """Create a new test client for each test function."""
    return app.test_client()


@pytest.fixture(scope="function")
def session(app):
    """Create a new database session for each test."""
    with app.app_context():
        db.session.begin_nested()
        yield db.session
        db.session.rollback()
