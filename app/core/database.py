from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.settings import Settings

TEST_MODE = Settings().TEST_MODE
engine = create_engine(Settings().DATABASE_URL if not TEST_MODE else Settings().TEST_DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
