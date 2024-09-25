from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Returns a database session object.

    Yields:
        Session: A database session object.

    Notes:
        The database session is automatically closed when it goes out of scope.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
