from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

sqllite_file_name = "database.db"
engine = create_engine(f"sqlite:///{sqllite_file_name}")

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Type alias for dependency injection of SQLModel Session using FastAPI's Depends
# This allows us to inject database sessions into route handlers
SessionDep = Annotated[Session, Depends(get_session)]