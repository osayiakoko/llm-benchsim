import uuid
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.sql import func
from src.database import Base


class BenchmarkResult(Base):
    __tablename__ = "benchmark_results"

    id = Column(PgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric = Column(String, index=True)
    llm_name = Column(String, index=True)
    mean_value = Column(Float)
    rank = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
