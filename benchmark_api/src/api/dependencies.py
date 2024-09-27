from fastapi import Depends
from sqlalchemy.orm import Session
from src.core.cache import RedisCache
from src.services import BenchmarkService
from src.repositories import BenchmarkRepository
from src.database import get_db
from src.config import settings


def get_benchmark_service(db: Session = Depends(get_db)):
    """
    Retrieves a BenchmarkService instance, which encapsulates the business logic for
    interacting with benchmark data. The service is initialized with a BenchmarkRepository
    instance, which is responsible for data access and caching.

    Args:
        db (Session): A SQLAlchemy session object, which is used to interact with the database.
            Defaults to the result of the get_db dependency.

    Returns:
        BenchmarkService: An instance of the BenchmarkService class, which provides methods
            for retrieving and manipulating benchmark data.
    """
    cache = RedisCache(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    return BenchmarkService(BenchmarkRepository(db, cache))
