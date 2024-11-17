from sqlmodel import SQLModel, create_engine, Session, select
from typing import Annotated, List, Type
from fastapi import Depends
from src.common.storage.storage import NewStorageHandler

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

class DBStorageHandler(NewStorageHandler):
    
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, model_type: Type[SQLModel]) -> List[SQLModel]:
        result = self.session.exec(select(model_type)).all()
        return list(result)

    def get_by_id(self, id: int, model_type: Type[SQLModel]) -> SQLModel:
        return self.session.get(model_type, id)

    def create(self, model: SQLModel) -> SQLModel:
        self.session.add(model)
        self.session.commit()
        return model

    def update(self, id: int, model: SQLModel) -> SQLModel:
        db_model = self.session.get(type(model), id)
        
        if not db_model:
            raise ValueError(f"{type(model).__name__} with id {id} not found")
        
        model_data = model.model_dump(exclude_unset=True)
        db_model.sqlmodel_update(model_data)
        self.session.add(db_model)
        self.session.commit()
        self.session.refresh(db_model)
        return db_model

    def delete(self, id: int, model_type: Type[SQLModel]) -> None:
        db_model = self.get_by_id(id, model_type)

        if not db_model:
            raise ValueError(f"Model with id {id} not found")
        
        self.session.delete(db_model)
        self.session.commit()