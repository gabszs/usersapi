from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.settings import Settings


def get_session():
    database_url = Settings().DATABASE_URL if not Settings().TEST_MODE else Settings().TEST_DATABASE_URL
    engine = create_engine(database_url)
    with Session(engine) as session:
        yield session
