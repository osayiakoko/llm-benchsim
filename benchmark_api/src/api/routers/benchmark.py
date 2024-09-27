from enum import Enum
from fastapi import APIRouter, Depends
from src.api.dependencies import get_benchmark_service
from src.core.security import get_api_key
from src.schemas import BenchmarkResultRead
from src.services import BenchmarkService


class ModelType(str, Enum):
    ttft = "TTFT"
    TPS = "TPS"
    e2e = "e2e_latency"
    rps = "RPS"


router = APIRouter(dependencies=[Depends(get_api_key)])


@router.get("/benchmark/{metric}", response_model=list[BenchmarkResultRead])
def get_benchmark(
    metric: ModelType,
    benchmark_service: BenchmarkService = Depends(get_benchmark_service),
):
    """
    Retrieves benchmark rankings for a given metric.

    Args:
        metric (ModelType): The metric to retrieve rankings for.
        benchmark_service (BenchmarkService): The service used to retrieve benchmark data.

    Returns:
        list[BenchmarkResultRead]: A list of benchmark rankings for the given metric.
    """
    rankings = benchmark_service.get_by_metric(metric)
    return rankings
