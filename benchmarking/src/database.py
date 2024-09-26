from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import settings

engine = create_engine(settings.EXTERNAL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.reflect(engine)


def get_db():
    """
    Returns a database session object that can be used to interact with the database.
    The session is created using the SessionLocal session maker and is configured to
    not autocommit or autoflush. The session is yielded within a try/finally block
    to ensure that it is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
