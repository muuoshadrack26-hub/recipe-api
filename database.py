from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

db_file="recipes.db"
engine=create_engine(f"sqlite:///{db_file}")

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    yield

SessionDep=Annotated[Session,Depends(get_session)]