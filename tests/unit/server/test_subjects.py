from src.common.models import DegreeName, Subject


def test_get_subjects(test_db, client):
    # Given
    subjects = [
        Subject(name="Math", degree=DegreeName.bachelor, semester=4),
        Subject(name="Physics", degree=DegreeName.master, semester=1),
        Subject(name="Chemistry", degree=DegreeName.bachelor, semester=4),
    ]
    for subject in subjects:
        test_db.add(subject)
    test_db.commit()

    # When
    response = client.get("/subjects")

    # Then
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == [subject.model_dump() for subject in subjects]


def test_get_subject(test_db, client):
    # Given
    subject = Subject(name="Math", degree=DegreeName.bachelor, semester=4)
    test_db.add(subject)
    test_db.commit()

    # When
    response = client.get(f"/subject/{subject.id}")

    # Then
    assert response.status_code == 200
    assert response.json() == subject.model_dump()


def test_get_subjects_in_degree(test_db, client):
    # Given
    subjects = [
        Subject(name="Math", degree=DegreeName.bachelor, semester=4),
        Subject(name="Physics", degree=DegreeName.master, semester=1),
        Subject(name="Chemistry", degree=DegreeName.bachelor, semester=4),
    ]
    for subject in subjects:
        test_db.add(subject)
    test_db.commit()

    # When
    response = client.get("/subjects?degree=Bachelor")

    # Then
    assert response.status_code == 200
    assert response.json() == [subjects[0].model_dump(), subjects[2].model_dump()]


def test_get_subjects_in_degree_and_semester(test_db, client):
    # Given
    subjects = [
        Subject(name="Math", degree=DegreeName.bachelor, semester=4),
        Subject(name="Physics", degree=DegreeName.master, semester=1),
        Subject(name="Chemistry", degree=DegreeName.bachelor, semester=4),
    ]
    for subject in subjects:
        test_db.add(subject)
    test_db.commit()

    # When
    response = client.get("/subjects?degree=Master&semester=1")

    # Then
    assert response.status_code == 200
    assert response.json() == [subjects[1].model_dump()]


def test_get_subjects_in_degree_and_semester_invalid(test_db, client):
    response = client.get("/subjects?degree=Bachelor&semester=10")
    assert response.status_code == 400
    assert response.json() == {"detail": "Bachelor degree has only 6 semesters"}

    response = client.get("/subjects?degree=Master&semester=10")
    assert response.status_code == 400
    assert response.json() == {"detail": "Master degree has only 4 semesters"}


def test_add_subject(test_db, client):
    response = client.post(
        "/subject", json={"name": "Math", "degree": "Bachelor", "semester": 4}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Math",
        "degree": "Bachelor",
        "semester": 4,
    }


def test_update_subject(test_db, client):
    subject = Subject(name="Math", degree=DegreeName.bachelor, semester=4)
    test_db.add(subject)
    test_db.commit()

    response = client.put(
        f"/subject/{subject.id}",
        json={"name": "Chemistry", "degree": "Bachelor", "semester": 4},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Chemistry",
        "degree": "Bachelor",
        "semester": 4,
    }


def test_update_subject_not_found(test_db, client):
    response = client.put(
        "/subject/1", json={"name": "Chemistry", "degree": "Bachelor", "semester": 4}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Subject with id 1 not found"}


def test_delete_subject(test_db, client):
    subject = Subject(name="Math", degree=DegreeName.bachelor, semester=4)
    test_db.add(subject)
    test_db.commit()

    response = client.delete(f"/subject/{subject.id}")
    assert response.status_code == 204


def test_delete_subject_not_found(test_db, client):
    response = client.delete("/subject/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Subject with id 1 not found"}
