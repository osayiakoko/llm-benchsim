from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Retrieves a database session object.

    Yields:
        Session: A SQLAlchemy session object, which is used to interact with the database.

    Notes:
        The database session is automatically closed after it is no longer needed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
