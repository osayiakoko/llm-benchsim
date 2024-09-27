from fastapi import FastAPI
from .benchmark import router as benchmark_router
from .root import router as root_router


def setup_routers(app: FastAPI) -> FastAPI:
    app.include_router(benchmark_router, prefix="/api/v1")
    app.include_router(root_router)

    return app
