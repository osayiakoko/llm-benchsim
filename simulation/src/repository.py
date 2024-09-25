from sqlalchemy.orm import Session

from src.models import SimulationResult
from src.schema import SimulationResultCreate


class SimulationRepository:
    def __init__(self, db: Session):
        """
        Initializes a SimulationRepository object.

        Args:
            db (Session): The database session to be used by the repository.

        Returns:
            None
        """
        self.db = db

    def insert_results(self, results: list[SimulationResultCreate]):
        """
        Inserts a list of simulation results into the database.

        Args:
            results (list[SimulationResultCreate]): A list of simulation results to be inserted.

        Returns:
            None
        """
        db_results = [SimulationResult(**result.model_dump()) for result in results]
        self.db.add_all(db_results)
        self.db.commit()
