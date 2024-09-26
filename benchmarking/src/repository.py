from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.schemas import BenchmarkResultCreate, BenchmarkResultRead
from src.models import BenchmarkResult
from src.logger import logger


class BenchmarkRepository:
    def __init__(self, db: Session):
        """
        Initializes a BenchmarkRepository instance.

        Args:
            db (Session): The SQLAlchemy ORM session.

        Returns:
            None
        """
        self.db = db

    def insert_results(self, results: list[BenchmarkResultCreate]):
        """
        Inserts a list of benchmark results into the database.

        Args:
            results (list[BenchmarkResultCreate]): A list of benchmark results to be inserted.

        Returns:
            None
        """
        try:
            with self.db.begin():
                # Delete existing benchmark results
                self.db.query(BenchmarkResult).delete()

                # Insert new benchmark results
                db_results = [
                    BenchmarkResult(**result.model_dump()) for result in results
                ]
                self.db.add_all(db_results)

        except SQLAlchemyError as e:
            logger.exception(e)

    def get_latest_results(self) -> list[BenchmarkResultRead]:
        """
        Retrieves the latest benchmark results from the database.

        This function queries the `BenchmarkResult` table in the database and retrieves all the records in descending order of the `timestamp` field. It returns a list of `BenchmarkResultRead` objects representing the latest benchmark results.

        Returns:
            list[BenchmarkResultRead]: A list of `BenchmarkResultRead` objects representing the latest benchmark results.
        """
        return (
            self.db.query(BenchmarkResult)
            .order_by(BenchmarkResult.timestamp.desc())
            .all()
        )
