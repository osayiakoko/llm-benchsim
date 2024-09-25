from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SimulationResultCreate(BaseModel):
    llm_name: str
    metric: str
    values: list[float]
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True
