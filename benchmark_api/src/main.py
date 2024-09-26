from fastapi import FastAPI
from src.database import Base



Base.metadata.create_all



app = FastAPI()