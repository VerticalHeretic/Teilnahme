from sqlmodel import SQLModel, create_engine, Session, select
from typing import Annotated, List, Type
from fastapi import Depends
from src.common.storage.storage import NewStorageHandler

# SQLite database configuration
sqllite_file_name = "database.db"
engine = create_engine(f"sqlite:///{sqllite_file_name}")


def get_session():
    """Create a new database session.

    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """Create database and tables based on SQLModel metadata."""
    SQLModel.metadata.create_all(engine)


# Type alias for dependency injection of SQLModel Session using FastAPI's Depends
# This allows us to inject database sessions into route handlers
SessionDep = Annotated[Session, Depends(get_session)]


class DBStorageHandler(NewStorageHandler):
    """Database storage handler implementation using SQLModel.

    This class implements the NewStorageHandler interface using SQLModel for database operations.
    """

    def __init__(self, session: Session):
        """Initialize DBStorageHandler with a database session.

        Args:
            session (Session): SQLModel database session
        """
        self.session = session

    def get_all(self, model_type: Type[SQLModel]) -> List[SQLModel]:
        """Get all models of the specified type.

        Args:
            model_type (Type[SQLModel]): The model class to query

        Returns:
            List[SQLModel]: List of all models of the specified type
        """
        result = self.session.exec(select(model_type)).all()
        return list(result)

    def get_by_id(self, id: int, model_type: Type[SQLModel]) -> SQLModel:
        """Get a model by its ID.

        Args:
            id (int): ID of the model to retrieve
            model_type (Type[SQLModel]): The model class to query

        Returns:
            SQLModel: The model with the specified ID

        Raises:
            ValueError: When model with given ID is not found
        """
        db_model = self.session.get(model_type, id)

        if not db_model:
            raise ValueError(f"{model_type.__name__} with id {id} not found")

        return db_model

    def get_all_where(self, model_type: Type[SQLModel], conditions) -> List[SQLModel]:
        """Get all models of given type that match the filter criteria.

        Example:
            # Get all students in semester 4
            students = storage.get_all_where(Student, semester=4)

            # Get all students named "John" in semester 4
            students = storage.get_all_where(Student, name="John", semester=4)

        Args:
            model_type (Type[SQLModel]): The model class to query
            **kwargs: Filter criteria as field=value pairs
                     e.g. semester=4, name="John"

        Returns:
            List[SQLModel]: List of matching models
        """
        result = self.session.exec(select(model_type).where(*conditions)).all()
        return list(result)

    def create(self, model: SQLModel) -> SQLModel:
        """Create a new model in the database.

        Args:
            model (SQLModel): Model instance to create

        Returns:
            SQLModel: The created model with updated fields (e.g. ID)
        """
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def update(self, id: int, model: SQLModel) -> SQLModel:
        """Update an existing model in the database.

        Args:
            id (int): ID of the model to update
            model (SQLModel): New model data

        Returns:
            SQLModel: The updated model

        Raises:
            ValueError: When model with given ID is not found
        """
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
        """Delete a model from the database.

        Args:
            id (int): ID of the model to delete
            model_type (Type[SQLModel]): The model class to delete from

        Raises:
            ValueError: When model with given ID is not found
        """
        db_model = self.get_by_id(id, model_type)

        if not db_model:
            raise ValueError(f"Model with id {id} not found")

        self.session.delete(db_model)
        self.session.commit()


def get_db_storage_handler(session: SessionDep) -> DBStorageHandler:
    """Create a DBStorageHandler instance with a database session.

    Args:
        session (SessionDep): Database session dependency

    Returns:
        DBStorageHandler: New DBStorageHandler instance configured with the session
    """
    return DBStorageHandler(session)


DBStorageHandlerDep = Annotated[DBStorageHandler, Depends(get_db_storage_handler)]
