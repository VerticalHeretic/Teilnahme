from multiprocessing import Value
import pytest
from sqlmodel import SQLModel, create_engine, Session

from src.common.storage.db_storage import DBStorageHandler
from src.common.models import Student, DegreeName

@pytest.fixture
def test_db(): 
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

class TestDBStorageHandler:
    def test_get_all(self, test_db):
        # Given
        for i in range(1, 4):
            test_db.add(Student(name=f"John {i}", surname=f"Doe {i}", degree=DegreeName.bachelor, semester=i))
        test_db.commit()
        storage_handler = DBStorageHandler(session=test_db)
        want = [Student(id=i, name=f"John {i}", surname=f"Doe {i}", degree=DegreeName.bachelor, semester=i) for i in range(1, 4)]

        # When
        got = storage_handler.get_all(Student)

        # Then
        assert got == want
    
    def test_get_all_empty(self, test_db):
        storage_handler = DBStorageHandler(session=test_db)
        assert storage_handler.get_all(Student) == []

    def test_get_by_id(self, test_db):
        # Given
        student = Student(name="John", surname="Doe", degree=DegreeName.bachelor, semester=1)
        test_db.add(student)
        test_db.commit()
        storage_handler = DBStorageHandler(session=test_db)
    
        # When
        got = storage_handler.get_by_id(1, Student)

        # Then
        assert got == student
    
    def test_get_by_id_not_found(self, test_db):
        storage_handler = DBStorageHandler(session=test_db)

        with pytest.raises(ValueError):
            storage_handler.get_by_id(1, Student)

    def test_create(self, test_db):
        # Given
        student = Student(name="John", surname="Doe", degree=DegreeName.bachelor, semester=1)
        storage_handler = DBStorageHandler(session=test_db)

        # When
        got = storage_handler.create(student)

        # Then
        assert got == student

    def test_delete(self, test_db):
        # Given
        student = Student(name="John", surname="Doe", degree=DegreeName.bachelor, semester=1)
        test_db.add(student)
        test_db.commit()
        storage_handler = DBStorageHandler(session=test_db)

        # When
        storage_handler.delete(1, Student)

        # Then
        with pytest.raises(ValueError):
            storage_handler.get_by_id(1, Student)
        
    def test_delete_not_existing(self, test_db):
        # Given
        storage_handler = DBStorageHandler(session=test_db)
        
        # When/Then
        with pytest.raises(ValueError):
            storage_handler.delete(1, Student)    
            
    def test_update(self, test_db):
        # Given
        student = Student(name="John", surname="Doe", degree=DegreeName.bachelor, semester=1)
        test_db.add(student)
        test_db.commit()
        storage_handler = DBStorageHandler(session=test_db) 

        # When
        got = storage_handler.update(1, Student(id=1, name="Jane", surname="Doe", degree=DegreeName.bachelor, semester=1))

        # Then
        assert got == Student(id=1, name="Jane", surname="Doe", degree=DegreeName.bachelor, semester=1)
    
    def test_update_not_existing(self, test_db):
        # Given
        storage_handler = DBStorageHandler(session=test_db)
        
        # When/Then
        with pytest.raises(ValueError):
            storage_handler.update(1, Student(id=1, name="John", surname="Doe", degree=DegreeName.bachelor, semester=1))    
    