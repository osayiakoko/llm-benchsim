import json
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.config import settings
from src.core.cache import RedisCache
from src.core.logging import logger
from src.models import BenchmarkResult
from src.schemas import BenchmarkResultRead


class BenchmarkRepository:
    def __init__(self, db: Session, cache: RedisCache):
        """
        Initializes a BenchmarkRepository instance with the given database session and Redis cache.

        Args:
            db (Session): A SQLAlchemy session object, which is used to interact with the database.
            cache (RedisCache): A RedisCache instance, which is used for caching benchmark results.

        Returns:
            None
        """
        self.db = db
        self.cache = cache

    def get_by_metric(self, metric: str) -> list[BenchmarkResultRead]:
        """
        Retrieves a list of benchmark results for a given metric.

        Args:
            metric (str): The metric to retrieve benchmark results for.

        Returns:
            list[BenchmarkResultRead]: A list of benchmark results for the given metric.

        Raises:
            HTTPException: If an error occurs during the retrieval process.
        """
        try:
            cache_key = f"benchmark:{metric}"

            cached_result = self.cache.get(cache_key)
            if cached_result:
                return [BenchmarkResult(**json.loads(item)) for item in cached_result]

            queryset = (
                self.db.query(BenchmarkResult)
                .filter(BenchmarkResult.metric == metric)
                .order_by(BenchmarkResult.rank)
                .all()
            )

            benchmarks = []

            if queryset:
                cache_items = []
                for item in queryset:
                    obj = BenchmarkResultRead(**item.__dict__)
                    benchmarks.append(obj)
                    cache_items.append(obj.model_dump_json())

                self.cache.set(
                    cache_key, cache_items, expiration=settings.CACHE_EXPIRATION
                )

            return benchmarks
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail=str("service not available"))
