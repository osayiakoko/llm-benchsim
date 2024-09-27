from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from src.api import APIResponse, setup_exceptions, setup_routers


def create_app(instrument: bool = True) -> FastAPI:
    app = FastAPI(default_response_class=APIResponse)

    app = setup_exceptions(app)
    app = setup_routers(app)

    if instrument:
        Instrumentator().instrument(app).expose(app)

    return app
