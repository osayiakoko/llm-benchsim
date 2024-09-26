# src/service/benchmarking_service.py
import json
import statistics
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.repository import BenchmarkRepository
from src.schemas import BenchmarkResultCreate, SimulationResultRead
from src.logger import logger


class BenchmarkingService:
    """
    Ranks the LLMs for each metric.
    Note that for TPS and RPS, higher values are better,
    while for TTFT and e2e_latency, lower values are better.
    """

    METRICS = ["TTFT", "TPS", "e2e_latency", "RPS"]

    def __init__(self, repository: BenchmarkRepository):
        """
        Initializes a BenchmarkingService instance.

        Args:
            repository (BenchmarkRepository): The repository instance to be used by the service.

        Returns:
            None
        """
        self.repository = repository

    def calculate_rankings(
        self, simulation_results: list[SimulationResultRead]
    ) -> dict[str, list[tuple[str, float, int]]]:
        """
        Calculates rankings for LLM performance metrics based on simulation results.

        Args:
            simulation_results (list[SimulationResultRead]): A list of simulation results.

        Returns:
            dict[str, list[tuple[str, float, int]]]: A dictionary of rankings where each key is
            a metric and each value is a list of tuples containing the LLM name, mean value, and rank.
        """
        rankings = {}
        for metric in set(result.metric for result in simulation_results):
            metric_results = [
                (result.llm_name, statistics.mean(result.values))
                for result in simulation_results
                if result.metric == metric
            ]
            sorted_results = sorted(
                metric_results, key=lambda x: x[1], reverse=metric in ["TPS", "RPS"]
            )
            rankings[metric] = [
                (llm, value, rank + 1)
                for rank, (llm, value) in enumerate(sorted_results)
            ]
        return rankings

    def store_rankings(self, rankings: dict):
        """
        Stores the calculated rankings for LLM performance metrics in the repository.

        Args:
            rankings (dict): A dictionary of rankings where each key is a metric and each
            value is a list of tuples containing the LLM name, mean value, and rank.

        Returns:
            None
        """
        timestamp = datetime.now(timezone.utc)
        results = []
        for metric, metric_rankings in rankings.items():
            for llm, mean_value, rank in metric_rankings:
                results.append(
                    BenchmarkResultCreate(
                        metric=metric,
                        llm_name=llm,
                        mean_value=mean_value,
                        rank=rank,
                        timestamp=timestamp,
                    )
                )
        self.repository.insert_results(results)
        logger.info(f"Stored {len(results)} benchmark results")

    def process_simulation_results(self, results: list[dict]):
        """
        Processes simulation results by converting them to SimulationResultRead objects,
        calculating rankings, storing the rankings, and logging the completion of the benchmarking process.

        Args:
            results (list[dict]): A list of simulation results.

        Returns:
            None
        """
        logger.info("Processing simulation results")
        simulation_results = [SimulationResultRead(**result) for result in results]
        rankings = self.calculate_rankings(simulation_results)
        self.store_rankings(rankings)
        logger.info("Benchmarking process completed")
