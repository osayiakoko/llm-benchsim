from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from typing import Optional


class BenchmarkResultRead(BaseModel):
    id: UUID4 = Field(default_factory=UUID4)
    metric: str
    llm_name: str
    mean_value: float
    rank: int
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True
