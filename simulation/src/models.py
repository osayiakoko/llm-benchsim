from sqlalchemy import Column, Integer, String, ARRAY, Float, DateTime
from sqlalchemy.sql import func
from src.database import Base


class SimulationResult(Base):
    __tablename__ = "simulation_results"

    id = Column(Integer, primary_key=True)
    llm_name = Column(String(50))
    metric = Column(String(20))
    values = Column(ARRAY(Float))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
