import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base

# Test database URL (fallback to default if TEST_DATABASE_URL is not set)
TEST_DATABASE_URL = "postgresql://postgres:postgres@test_db:5432/test_db"


# Set up a test database engine and session
test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def setup_test_db():
    """Set up and tear down the test database schema for the session."""
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    yield
    # Drop all tables after the test session
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session(setup_test_db):
    """
    Provide a clean database session for each test.
    Uses transactions to isolate tests and rolls back changes after each test.
    """
    connection = test_engine.connect()
    transaction = connection.begin()  # Start a transaction

    # Create a new session bound to the connection
    session = TestSessionLocal(bind=connection)
    try:
        yield session  # Provide the session to the test
    finally:
        session.close()  # Close the session
        transaction.rollback()  # Roll back the transaction
        connection.close()  # Close the connection
