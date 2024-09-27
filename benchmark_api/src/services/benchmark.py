from src.models import BenchmarkResult
from src.repositories import BenchmarkRepository


class BenchmarkService:
    def __init__(self, repository: BenchmarkRepository):
        """
        Initializes a BenchmarkService instance with the given BenchmarkRepository.

        Args:
            repository (BenchmarkRepository): The repository used for data access and caching.

        Returns:
            None
        """
        self.repository = repository

    def get_by_metric(self, metric: str) -> list[BenchmarkResult]:
        """
        Retrieves a list of benchmark results for a given metric.

        Args:
            metric (str): The metric to retrieve benchmark results for.

        Returns:
            list[BenchmarkResult]: A list of benchmark results for the given metric.
        """
        return self.repository.get_by_metric(metric)
