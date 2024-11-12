from fastapi import FastAPI, status
from enum import Enum
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

class ClassName(str, Enum):
    son = "Specjalistyczne Oprogramowanie Narzędziowe"
    dpp = "Dobre Praktyki Programowania"

class DegreeName(str, Enum):
    master = "Master"
    bachelor = "Bachelor"

class BaseStudent(BaseModel):
    name: str
    surname: str
    degree: DegreeName
    semester: int

class Student(BaseStudent):
    id: int

fake_students_db = [
    Student(id=1, name="John", surname="Owens", degree=DegreeName.bachelor, semester=3),
    Student(id=2, name="Jane", surname="Doe", degree=DegreeName.bachelor, semester=1),
    Student(id=3, name="Alice", surname="Smith", degree=DegreeName.bachelor, semester=2),
    Student(id=4, name="Bob", surname="Brown", degree=DegreeName.bachelor, semester=4),
    Student(id=5, name="Charlie", surname="Davis", degree=DegreeName.bachelor, semester=5),
    Student(id=6, name="Eve", surname="Miller", degree=DegreeName.bachelor, semester=6),
    Student(id=7, name="Frank", surname="Wilson", degree=DegreeName.bachelor, semester=3),
    Student(id=8, name="Grace", surname="Moore", degree=DegreeName.bachelor, semester=1),
    Student(id=9, name="Hank", surname="Taylor", degree=DegreeName.bachelor, semester=2),
    Student(id=10, name="Ivy", surname="Anderson", degree=DegreeName.bachelor, semester=4),
    Student(id=11, name="Jack", surname="Thomas", degree=DegreeName.bachelor, semester=5),
    Student(id=12, name="Kara", surname="Jackson", degree=DegreeName.bachelor, semester=6),
    Student(id=13, name="Leo", surname="White", degree=DegreeName.bachelor, semester=3),
    Student(id=14, name="Mia", surname="Harris", degree=DegreeName.bachelor, semester=1),
    Student(id=15, name="Nina", surname="Martin", degree=DegreeName.bachelor, semester=2),
    Student(id=16, name="Oscar", surname="Thompson", degree=DegreeName.bachelor, semester=4),
    Student(id=17, name="Paul", surname="Garcia", degree=DegreeName.bachelor, semester=5),
    Student(id=18, name="Quinn", surname="Martinez", degree=DegreeName.bachelor, semester=6),
    Student(id=19, name="Rose", surname="Robinson", degree=DegreeName.bachelor, semester=3),
    Student(id=20, name="Sam", surname="Clark", degree=DegreeName.bachelor, semester=1),
    Student(id=21, name="Tina", surname="Rodriguez", degree=DegreeName.bachelor, semester=2),
    Student(id=22, name="Uma", surname="Lewis", degree=DegreeName.bachelor, semester=4),
    Student(id=23, name="Vince", surname="Lee", degree=DegreeName.bachelor, semester=5),
    Student(id=24, name="Wendy", surname="Walker", degree=DegreeName.bachelor, semester=6),
    Student(id=25, name="Xander", surname="Hall", degree=DegreeName.bachelor, semester=3),
    Student(id=26, name="Yara", surname="Allen", degree=DegreeName.bachelor, semester=1),
    Student(id=27, name="Zane", surname="Young", degree=DegreeName.bachelor, semester=2),
    Student(id=28, name="Amy", surname="King", degree=DegreeName.bachelor, semester=4),
    Student(id=29, name="Brian", surname="Scott", degree=DegreeName.bachelor, semester=5),
    Student(id=30, name="Cathy", surname="Green", degree=DegreeName.bachelor, semester=6),
    Student(id=31, name="David", surname="Adams", degree=DegreeName.bachelor, semester=3),
    Student(id=32, name="Ella", surname="Baker", degree=DegreeName.bachelor, semester=1),
    Student(id=33, name="Fiona", surname="Gonzalez", degree=DegreeName.bachelor, semester=2),
    Student(id=34, name="George", surname="Nelson", degree=DegreeName.bachelor, semester=4),
    Student(id=35, name="Holly", surname="Carter", degree=DegreeName.bachelor, semester=5),
    Student(id=36, name="Ian", surname="Mitchell", degree=DegreeName.bachelor, semester=6),
    Student(id=37, name="Jill", surname="Perez", degree=DegreeName.bachelor, semester=3),
    Student(id=38, name="Kyle", surname="Roberts", degree=DegreeName.bachelor, semester=1),
    Student(id=39, name="Liam", surname="Turner", degree=DegreeName.bachelor, semester=2),
    Student(id=40, name="Mona", surname="Phillips", degree=DegreeName.bachelor, semester=4),
    Student(id=41, name="Nate", surname="Campbell", degree=DegreeName.bachelor, semester=5),
    Student(id=42, name="Olivia", surname="Parker", degree=DegreeName.bachelor, semester=6),
    Student(id=43, name="Pete", surname="Evans", degree=DegreeName.bachelor, semester=3),
    Student(id=44, name="Quincy", surname="Edwards", degree=DegreeName.bachelor, semester=1),
    Student(id=45, name="Rachel", surname="Collins", degree=DegreeName.bachelor, semester=2),
    Student(id=46, name="Steve", surname="Stewart", degree=DegreeName.bachelor, semester=4),
    Student(id=47, name="Tara", surname="Sanchez", degree=DegreeName.bachelor, semester=5),
    Student(id=48, name="Ursula", surname="Morris", degree=DegreeName.bachelor, semester=6),
    Student(id=49, name="Victor", surname="Rogers", degree=DegreeName.bachelor, semester=3),
    Student(id=50, name="Wade", surname="Reed", degree=DegreeName.bachelor, semester=1),
    Student(id=51, name="Xena", surname="Cook", degree=DegreeName.bachelor, semester=2),
    Student(id=52, name="Yvonne", surname="Morgan", degree=DegreeName.bachelor, semester=4),
    Student(id=53, name="Zach", surname="Bell", degree=DegreeName.bachelor, semester=5),
    Student(id=54, name="Aaron", surname="Murphy", degree=DegreeName.master, semester=1),
    Student(id=55, name="Betty", surname="Bailey", degree=DegreeName.master, semester=2),
    Student(id=56, name="Carl", surname="Rivera", degree=DegreeName.master, semester=3),
    Student(id=57, name="Diana", surname="Cooper", degree=DegreeName.master, semester=4),
    Student(id=58, name="Ethan", surname="Richardson", degree=DegreeName.master, semester=1),
    Student(id=59, name="Faye", surname="Cox", degree=DegreeName.master, semester=2),
    Student(id=60, name="Gina", surname="Howard", degree=DegreeName.master, semester=3),
    Student(id=61, name="Hugo", surname="Ward", degree=DegreeName.master, semester=4),
    Student(id=62, name="Iris", surname="Torres", degree=DegreeName.master, semester=1),
    Student(id=63, name="Jake", surname="Peterson", degree=DegreeName.master, semester=2),
    Student(id=64, name="Kara", surname="Gray", degree=DegreeName.master, semester=3),
    Student(id=65, name="Lana", surname="Ramirez", degree=DegreeName.master, semester=4),
    Student(id=66, name="Mike", surname="James", degree=DegreeName.master, semester=1),
    Student(id=67, name="Nora", surname="Watson", degree=DegreeName.master, semester=2),
    Student(id=68, name="Omar", surname="Brooks", degree=DegreeName.master, semester=3),
    Student(id=69, name="Paula", surname="Kelly", degree=DegreeName.master, semester=4),
    Student(id=70, name="Quinn", surname="Sanders", degree=DegreeName.master, semester=1),
    Student(id=71, name="Rita", surname="Price", degree=DegreeName.master, semester=2),
    Student(id=72, name="Sean", surname="Bennett", degree=DegreeName.master, semester=3),
    Student(id=73, name="Tina", surname="Wood", degree=DegreeName.master, semester=4),
    Student(id=74, name="Uma", surname="Barnes", degree=DegreeName.master, semester=1),
    Student(id=75, name="Vince", surname="Ross", degree=DegreeName.master, semester=2),
    Student(id=76, name="Wendy", surname="Henderson", degree=DegreeName.master, semester=3),
    Student(id=77, name="Xander", surname="Coleman", degree=DegreeName.master, semester=4),
    Student(id=78, name="Yara", surname="Jenkins", degree=DegreeName.master, semester=1),
    Student(id=79, name="Zane", surname="Perry", degree=DegreeName.master, semester=2),
    Student(id=80, name="Amy", surname="Powell", degree=DegreeName.master, semester=3),
    Student(id=81, name="Brian", surname="Long", degree=DegreeName.master, semester=4),
    Student(id=82, name="Cathy", surname="Patterson", degree=DegreeName.master, semester=1),
    Student(id=83, name="David", surname="Hughes", degree=DegreeName.master, semester=2),
    Student(id=84, name="Ella", surname="Flores", degree=DegreeName.master, semester=3),
    Student(id=85, name="Fiona", surname="Washington", degree=DegreeName.master, semester=4),
    Student(id=86, name="George", surname="Butler", degree=DegreeName.master, semester=1),
    Student(id=87, name="Holly", surname="Simmons", degree=DegreeName.master, semester=2),
    Student(id=88, name="Ian", surname="Foster", degree=DegreeName.master, semester=3),
    Student(id=89, name="Jill", surname="Gonzales", degree=DegreeName.master, semester=4)
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
async def add_student(student: BaseStudent) -> list[Student]:
    last_id = fake_students_db[-1].id

    fake_students_db.append(Student(id=last_id+1, name=student.name, surname=student.surname, degree=student.degree, semester=student.semester))
    return fake_students_db

@app.put("/students/{student_id}", status_code=status.HTTP_200_OK)
async def update_student(student_id: int, updated_student: BaseStudent) -> Student:
    student_index = next((index for index, student in enumerate(fake_students_db)
                        if student.id == student_id), None)

    if student_index is None:
        raise HTTPException(status_code=404, detail="The is no such student")

    student = fake_students_db[student_index]

    student.name = updated_student.name
    student.surname = updated_student.surname
    student.degree = updated_student.degree
    student.semester = updated_student.semester

    fake_students_db[student_index] = student

    return student

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int):
    student = next((student for student in fake_students_db if student.id == student_id))

    if student is None:
        raise HTTPException(status_code=404, detail="The is no such student")

    fake_students_db.remove(student)
