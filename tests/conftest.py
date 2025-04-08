import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.models.base import Base
from app.core.settings import get_settings, Settings
from app.server.main import create_app

settings: Settings = get_settings()

engine = create_engine("postgresql+psycopg2://" + settings.get_postgres_url)

TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="session", autouse=True)
def db_session():
    session = TestingSession()
    yield session
    session.close()


@pytest.fixture(scope="session", autouse=True)
def set_up_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def http_client():
    print("HTTP client started successfully\n")
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client
