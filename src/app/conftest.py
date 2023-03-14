import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from fastapi.testclient import TestClient
import typing as t

from app import mock
from app.api import auth, schemas
from app.db import models
from app.db.session import Base
from app.main import app
from app.config import TEST_DB_CONNECTION_STR, Scopes


@pytest.fixture
def db_connection():
    """
    returns a connection that persists across tests
    """
    engine = create_engine(TEST_DB_CONNECTION_STR)

    connection = engine.connect()

    # Run a parent transaction that can roll back all changes
    test_session_maker = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    test_session = test_session_maker()
    seed_database(test_session)
    yield test_session

    test_session.close()
    connection.close()


@pytest.fixture
def test_db():
    """
    Modify the db session to automatically roll back after each test.
    This is to avoid tests affecting the database state of other tests.
    """
    # Connect to the test database
    print(TEST_DB_CONNECTION_STR)
    engine = create_engine(TEST_DB_CONNECTION_STR)

    connection = engine.connect()
    trans = connection.begin()

    # Run a parent transaction that can roll back all changes
    test_session_maker = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    test_session = test_session_maker()
    test_session.begin_nested()

    @event.listens_for(test_session, "after_transaction_end")
    def restart_savepoint(s, transaction):
        if transaction.nested and not transaction._parent.nested:
            s.expire_all()
            s.begin_nested()

    yield test_session

    # Roll back the parent transaction after the test is complete
    test_session.close()
    trans.rollback()
    connection.close()


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    """
    Create a test database and use it for the whole test session.
    """
    # Create the test database
    # if database_exists(TEST_DB_CONNECTION_STR):
    #     drop_database(TEST_DB_CONNECTION_STR)

    create_database(TEST_DB_CONNECTION_STR)
    test_engine = create_engine(TEST_DB_CONNECTION_STR)
    Base.metadata.create_all(test_engine)

    # Run the tests
    yield

    # Drop the test database
    drop_database(TEST_DB_CONNECTION_STR)


@pytest.fixture
def get_user(client, user_token_headers):
    req = client.get("/api/v1/users/me", headers=user_token_headers)
    return schemas.UserOut(**req.json())


@pytest.fixture
def client():
    """
    Get a TestClient instance that reads/write to the test database.
    """

    yield TestClient(app)


@pytest.fixture
def test_password() -> str:
    return "securepassword"


def get_password_hash() -> str:
    """
    Password hashing can be expensive so a mock will be much faster
    """
    return "supersecrethash"


@pytest.fixture
def test_user(db_connection) -> models.User:
    """
    Make a test user in the database
    """
    user = (
        db_connection.query(models.User)
        .filter(models.User.email == "fake@email.com")
        .first()
    )
    if user:
        return user
    user = models.User(
        email="fake@email.com",
        password=get_password_hash(),
        scopes=Scopes.USER,
        is_disabled=False
    )
    db_connection.add(user)
    db_connection.commit()
    return user


@pytest.fixture
def test_superuser(db_connection) -> models.User:
    """
    Superuser for testing
    """
    user = (
        db_connection.query(models.User)
        .filter(models.User.email == "fakeadmin@email.com")
        .first()
    )
    if user:
        return user
    user = models.User(
        email="fakeadmin@email.com",
        password=get_password_hash(),
        scopes=' '.join([Scopes.ADMIN, Scopes.USER]),
        is_disabled=False,
        is_deleted=False
    )
    db_connection.add(user)
    db_connection.commit()
    db_connection.refresh(user)
    return user


def verify_password_mock(first: str, second: str) -> bool:
    return True


def verify_password_failed_mock(first: str, second: str) -> bool:
    return False


def get_auth_tokens(client: TestClient, data, monkeypatch):
    monkeypatch.setattr(auth, "verify_password", verify_password_mock)
    r = client.post("/api/v1/token", data=data)
    res = r.json()
    token = res["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def user_token_headers(
    client: TestClient, test_user, test_password, monkeypatch
) -> t.Dict[str, str]:
    login_data = {
        "username": test_user.email,
        "password": test_password,
    }
    return get_auth_tokens(client, login_data, monkeypatch)


@pytest.fixture
def superuser_token_headers(
    client: TestClient, test_superuser, test_password, monkeypatch
) -> t.Dict[str, str]:
    login_data = {
        "username": test_superuser.email,
        "password": test_password,
    }
    return get_auth_tokens(client, login_data, monkeypatch)


def seed_database(db_connection):
    '''
        This function seeds metadata into the database that persists
        across all tests.  Think about this more like metadata that doens't
        really ever change vs test specific data
    '''
    tables = [
        # Add tuple (model, mock_data)
    ]
    for table in tables:
        mock.seed_table(table[0], table[1], db_connection)
