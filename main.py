from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

class ClassName(str, Enum):
    son = "Specjalistyczne Oprogramowanie Narzędziowe"
    dpp = "Dobre Praktyki Programowania"

class DegreeName(str, Enum):
    master = "Master"
    bachelor = "Bachelor"

class Student(BaseModel):
    name: str
    surname: str
    degree: DegreeName
    semester: int

fake_students_db = [
    Student(name="John", surname="Owens", degree=DegreeName.bachelor, semester=3),
    Student(name="Jane", surname="Doe", degree=DegreeName.bachelor, semester=1),
    Student(name="Alice", surname="Smith", degree=DegreeName.bachelor, semester=2),
    Student(name="Bob", surname="Brown", degree=DegreeName.bachelor, semester=4),
    Student(name="Charlie", surname="Davis", degree=DegreeName.bachelor, semester=5),
    Student(name="Eve", surname="Miller", degree=DegreeName.bachelor, semester=6),
    Student(name="Frank", surname="Wilson", degree=DegreeName.bachelor, semester=3),
    Student(name="Grace", surname="Moore", degree=DegreeName.bachelor, semester=1),
    Student(name="Hank", surname="Taylor", degree=DegreeName.bachelor, semester=2),
    Student(name="Ivy", surname="Anderson", degree=DegreeName.bachelor, semester=4),
    Student(name="Jack", surname="Thomas", degree=DegreeName.bachelor, semester=5),
    Student(name="Kara", surname="Jackson", degree=DegreeName.bachelor, semester=6),
    Student(name="Leo", surname="White", degree=DegreeName.bachelor, semester=3),
    Student(name="Mia", surname="Harris", degree=DegreeName.bachelor, semester=1),
    Student(name="Nina", surname="Martin", degree=DegreeName.bachelor, semester=2),
    Student(name="Oscar", surname="Thompson", degree=DegreeName.bachelor, semester=4),
    Student(name="Paul", surname="Garcia", degree=DegreeName.bachelor, semester=5),
    Student(name="Quinn", surname="Martinez", degree=DegreeName.bachelor, semester=6),
    Student(name="Rose", surname="Robinson", degree=DegreeName.bachelor, semester=3),
    Student(name="Sam", surname="Clark", degree=DegreeName.bachelor, semester=1),
    Student(name="Tina", surname="Rodriguez", degree=DegreeName.bachelor, semester=2),
    Student(name="Uma", surname="Lewis", degree=DegreeName.bachelor, semester=4),
    Student(name="Vince", surname="Lee", degree=DegreeName.bachelor, semester=5),
    Student(name="Wendy", surname="Walker", degree=DegreeName.bachelor, semester=6),
    Student(name="Xander", surname="Hall", degree=DegreeName.bachelor, semester=3),
    Student(name="Yara", surname="Allen", degree=DegreeName.bachelor, semester=1),
    Student(name="Zane", surname="Young", degree=DegreeName.bachelor, semester=2),
    Student(name="Amy", surname="King", degree=DegreeName.bachelor, semester=4),
    Student(name="Brian", surname="Scott", degree=DegreeName.bachelor, semester=5),
    Student(name="Cathy", surname="Green", degree=DegreeName.bachelor, semester=6),
    Student(name="David", surname="Adams", degree=DegreeName.bachelor, semester=3),
    Student(name="Ella", surname="Baker", degree=DegreeName.bachelor, semester=1),
    Student(name="Fiona", surname="Gonzalez", degree=DegreeName.bachelor, semester=2),
    Student(name="George", surname="Nelson", degree=DegreeName.bachelor, semester=4),
    Student(name="Holly", surname="Carter", degree=DegreeName.bachelor, semester=5),
    Student(name="Ian", surname="Mitchell", degree=DegreeName.bachelor, semester=6),
    Student(name="Jill", surname="Perez", degree=DegreeName.bachelor, semester=3),
    Student(name="Kyle", surname="Roberts", degree=DegreeName.bachelor, semester=1),
    Student(name="Liam", surname="Turner", degree=DegreeName.bachelor, semester=2),
    Student(name="Mona", surname="Phillips", degree=DegreeName.bachelor, semester=4),
    Student(name="Nate", surname="Campbell", degree=DegreeName.bachelor, semester=5),
    Student(name="Olivia", surname="Parker", degree=DegreeName.bachelor, semester=6),
    Student(name="Pete", surname="Evans", degree=DegreeName.bachelor, semester=3),
    Student(name="Quincy", surname="Edwards", degree=DegreeName.bachelor, semester=1),
    Student(name="Rachel", surname="Collins", degree=DegreeName.bachelor, semester=2),
    Student(name="Steve", surname="Stewart", degree=DegreeName.bachelor, semester=4),
    Student(name="Tara", surname="Sanchez", degree=DegreeName.bachelor, semester=5),
    Student(name="Ursula", surname="Morris", degree=DegreeName.bachelor, semester=6),
    Student(name="Victor", surname="Rogers", degree=DegreeName.bachelor, semester=3),
    Student(name="Wade", surname="Reed", degree=DegreeName.bachelor, semester=1),
    Student(name="Xena", surname="Cook", degree=DegreeName.bachelor, semester=2),
    Student(name="Yvonne", surname="Morgan", degree=DegreeName.bachelor, semester=4),
    Student(name="Zach", surname="Bell", degree=DegreeName.bachelor, semester=5),
    Student(name="Aaron", surname="Murphy", degree=DegreeName.master, semester=1),
    Student(name="Betty", surname="Bailey", degree=DegreeName.master, semester=2),
    Student(name="Carl", surname="Rivera", degree=DegreeName.master, semester=3),
    Student(name="Diana", surname="Cooper", degree=DegreeName.master, semester=4),
    Student(name="Ethan", surname="Richardson", degree=DegreeName.master, semester=1),
    Student(name="Faye", surname="Cox", degree=DegreeName.master, semester=2),
    Student(name="Gina", surname="Howard", degree=DegreeName.master, semester=3),
    Student(name="Hugo", surname="Ward", degree=DegreeName.master, semester=4),
    Student(name="Iris", surname="Torres", degree=DegreeName.master, semester=1),
    Student(name="Jake", surname="Peterson", degree=DegreeName.master, semester=2),
    Student(name="Kara", surname="Gray", degree=DegreeName.master, semester=3),
    Student(name="Lana", surname="Ramirez", degree=DegreeName.master, semester=4),
    Student(name="Mike", surname="James", degree=DegreeName.master, semester=1),
    Student(name="Nora", surname="Watson", degree=DegreeName.master, semester=2),
    Student(name="Omar", surname="Brooks", degree=DegreeName.master, semester=3),
    Student(name="Paula", surname="Kelly", degree=DegreeName.master, semester=4),
    Student(name="Quinn", surname="Sanders", degree=DegreeName.master, semester=1),
    Student(name="Rita", surname="Price", degree=DegreeName.master, semester=2),
    Student(name="Sean", surname="Bennett", degree=DegreeName.master, semester=3),
    Student(name="Tina", surname="Wood", degree=DegreeName.master, semester=4),
    Student(name="Uma", surname="Barnes", degree=DegreeName.master, semester=1),
    Student(name="Vince", surname="Ross", degree=DegreeName.master, semester=2),
    Student(name="Wendy", surname="Henderson", degree=DegreeName.master, semester=3),
    Student(name="Xander", surname="Coleman", degree=DegreeName.master, semester=4),
    Student(name="Yara", surname="Jenkins", degree=DegreeName.master, semester=1),
    Student(name="Zane", surname="Perry", degree=DegreeName.master, semester=2),
    Student(name="Amy", surname="Powell", degree=DegreeName.master, semester=3),
    Student(name="Brian", surname="Long", degree=DegreeName.master, semester=4),
    Student(name="Cathy", surname="Patterson", degree=DegreeName.master, semester=1),
    Student(name="David", surname="Hughes", degree=DegreeName.master, semester=2),
    Student(name="Ella", surname="Flores", degree=DegreeName.master, semester=3),
    Student(name="Fiona", surname="Washington", degree=DegreeName.master, semester=4),
    Student(name="George", surname="Butler", degree=DegreeName.master, semester=1),
    Student(name="Holly", surname="Simmons", degree=DegreeName.master, semester=2),
    Student(name="Ian", surname="Foster", degree=DegreeName.master, semester=3),
    Student(name="Jill", surname="Gonzales", degree=DegreeName.master, semester=4)
]

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int):
    return {"user_id": user_id}

# Path parameters example
@app.get("/classes/{class_name}")
async def get_class(class_name: ClassName):
    if class_name is ClassName.son:
        return {"model_name": class_name, "message": "Licencjat for the win!"}
    elif class_name is ClassName.dpp:
        return {"model_name": class_name, "message": "Magisterka for the win!"}

    return  {"model_name": class_name, "message": "No win for you :("}

# Path and Query operators example
@app.get("/students/{degree_name}")
async def get_students_in_degree(degree_name: DegreeName, semester: int | None = None) -> list[Student]:
    if degree_name is DegreeName.bachelor and semester is int and semester > 6:
        return {"message": "Bachelor degree has only 6 semesters"}
    elif degree_name is DegreeName.master and semester is int and semester > 4:
        return {"message": "Master degree has only 4 semesters"}

    filtered_students = filter(lambda student: student.degree == degree_name, fake_students_db)

    if semester is not None:
        filtered_students = filter(lambda student: student.semester == semester, fake_students_db)

    return list(filtered_students)

@app.post("/students/")
async def add_student(student: Student) -> list[Student]:
    fake_students_db.append(student)
    return fake_students_db
