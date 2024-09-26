import uuid
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from src.database import Base


class BenchmarkResult(Base):
    __tablename__ = "benchmark_results"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric = Column(String, index=True)
    llm_name = Column(String, index=True)
    mean_value = Column(Float)
    rank = Column(Integer, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
