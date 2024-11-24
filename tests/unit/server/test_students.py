import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel, StaticPool

from src.common.models import DegreeName, Student
from src.common.storage.db_storage import get_session
from src.server.server import app


@pytest.fixture
def test_db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(test_db):
    app.dependency_overrides[get_session] = lambda: test_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


def test_get_students(test_db, client):
    # Given
    students = [
        Student(name="John", surname="Daw", degree=DegreeName.bachelor, semester=4),
        Student(name="Joe", surname="Daw", degree=DegreeName.bachelor, semester=4),
        Student(name="Hank", surname="Daw", degree=DegreeName.bachelor, semester=4),
    ]
    for student in students:
        test_db.add(student)
    test_db.commit()

    # When
    response = client.get("/students")

    # Then
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == [
        {
            "id": 1,
            "name": "John",
            "surname": "Daw",
            "degree": "Bachelor",
            "semester": 4,
        },
        {"id": 2, "name": "Joe", "surname": "Daw", "degree": "Bachelor", "semester": 4},
        {
            "id": 3,
            "name": "Hank",
            "surname": "Daw",
            "degree": "Bachelor",
            "semester": 4,
        },
    ]


def test_get_students_in_degree(test_db, client):
    # Given
    students = [
        Student(name="John", surname="Daw", degree=DegreeName.bachelor, semester=3),
        Student(name="Joe", surname="Daw", degree=DegreeName.bachelor, semester=4),
        Student(name="Hank", surname="Daw", degree=DegreeName.master, semester=4),
    ]
    for student in students:
        test_db.add(student)
    test_db.commit()

    # When
    response = client.get("/students?degree=Bachelor")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "John",
            "surname": "Daw",
            "degree": "Bachelor",
            "semester": 3,
        },
        {
            "id": 2,
            "name": "Joe",
            "surname": "Daw",
            "degree": "Bachelor",
            "semester": 4,
        },
    ]


def test_get_students_in_degree_with_semester(test_db, client):
    # Given
    students = [
        Student(name="John", surname="Daw", degree=DegreeName.bachelor, semester=3),
        Student(name="Joe", surname="Daw", degree=DegreeName.bachelor, semester=4),
        Student(name="Hank", surname="Daw", degree=DegreeName.master, semester=4),
    ]
    for student in students:
        test_db.add(student)
    test_db.commit()

    # When
    response = client.get("/students?degree=Bachelor&semester=3")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "John",
            "surname": "Daw",
            "degree": "Bachelor",
            "semester": 3,
        }
    ]


def test_get_students_in_degree_with_invalid_semester(client):
    response = client.get("/students?degree=Bachelor&semester=10")
    assert response.status_code == 400
    assert response.json() == {"detail": "Bachelor degree has only 6 semesters"}

    response = client.get("/students?degree=Master&semester=10")
    assert response.status_code == 400
    assert response.json() == {"detail": "Master degree has only 4 semesters"}


def test_add_student(client):
    response = client.post(
        "/students",
        json={"name": "John", "surname": "Daw", "degree": "Bachelor", "semester": 4},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "John",
        "surname": "Daw",
        "degree": "Bachelor",
        "semester": 4,
    }


def test_update_student(test_db, client):
    test_db.add(
        Student(name="John", surname="Daw", degree=DegreeName.bachelor, semester=4)
    )
    test_db.commit()

    response = client.put(
        "/students/1",
        json={"name": "Patrick", "surname": "Jane", "degree": "Master", "semester": 3},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Patrick",
        "surname": "Jane",
        "degree": "Master",
        "semester": 3,
    }


def test_delete_student(test_db, client):
    test_db.add(
        Student(name="John", surname="Daw", degree=DegreeName.bachelor, semester=4)
    )
    test_db.commit()

    response = client.delete("/students/1")
    assert response.status_code == 204
