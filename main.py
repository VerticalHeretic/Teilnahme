from fastapi import FastAPI
from enum import Enum

class ClassName(str, Enum):
    son = "Specjalistyczne Oprogramowanie Narzędziowe"
    dpp = "Dobre Praktyki Programowania"

class DegreeName(str, Enum):
    master = "Master"
    bachelor = "Bachelor"

fake_students_db = [
    {"name": "John", "surname": "Owens", "degree": "Bachelor", "semester": 3},
    {"name": "Jane", "surname": "Doe", "degree": "Bachelor", "semester": 1},
    {"name": "Alice", "surname": "Smith", "degree": "Bachelor", "semester": 2},
    {"name": "Bob", "surname": "Brown", "degree": "Bachelor", "semester": 4},
    {"name": "Charlie", "surname": "Davis", "degree": "Bachelor", "semester": 5},
    {"name": "Eve", "surname": "Miller", "degree": "Bachelor", "semester": 6},
    {"name": "Frank", "surname": "Wilson", "degree": "Bachelor", "semester": 3},
    {"name": "Grace", "surname": "Moore", "degree": "Bachelor", "semester": 1},
    {"name": "Hank", "surname": "Taylor", "degree": "Bachelor", "semester": 2},
    {"name": "Ivy", "surname": "Anderson", "degree": "Bachelor", "semester": 4},
    {"name": "Jack", "surname": "Thomas", "degree": "Bachelor", "semester": 5},
    {"name": "Kara", "surname": "Jackson", "degree": "Bachelor", "semester": 6},
    {"name": "Leo", "surname": "White", "degree": "Bachelor", "semester": 3},
    {"name": "Mia", "surname": "Harris", "degree": "Bachelor", "semester": 1},
    {"name": "Nina", "surname": "Martin", "degree": "Bachelor", "semester": 2},
    {"name": "Oscar", "surname": "Thompson", "degree": "Bachelor", "semester": 4},
    {"name": "Paul", "surname": "Garcia", "degree": "Bachelor", "semester": 5},
    {"name": "Quinn", "surname": "Martinez", "degree": "Bachelor", "semester": 6},
    {"name": "Rose", "surname": "Robinson", "degree": "Bachelor", "semester": 3},
    {"name": "Sam", "surname": "Clark", "degree": "Bachelor", "semester": 1},
    {"name": "Tina", "surname": "Rodriguez", "degree": "Bachelor", "semester": 2},
    {"name": "Uma", "surname": "Lewis", "degree": "Bachelor", "semester": 4},
    {"name": "Vince", "surname": "Lee", "degree": "Bachelor", "semester": 5},
    {"name": "Wendy", "surname": "Walker", "degree": "Bachelor", "semester": 6},
    {"name": "Xander", "surname": "Hall", "degree": "Bachelor", "semester": 3},
    {"name": "Yara", "surname": "Allen", "degree": "Bachelor", "semester": 1},
    {"name": "Zane", "surname": "Young", "degree": "Bachelor", "semester": 2},
    {"name": "Amy", "surname": "King", "degree": "Bachelor", "semester": 4},
    {"name": "Brian", "surname": "Scott", "degree": "Bachelor", "semester": 5},
    {"name": "Cathy", "surname": "Green", "degree": "Bachelor", "semester": 6},
    {"name": "David", "surname": "Adams", "degree": "Bachelor", "semester": 3},
    {"name": "Ella", "surname": "Baker", "degree": "Bachelor", "semester": 1},
    {"name": "Fiona", "surname": "Gonzalez", "degree": "Bachelor", "semester": 2},
    {"name": "George", "surname": "Nelson", "degree": "Bachelor", "semester": 4},
    {"name": "Holly", "surname": "Carter", "degree": "Bachelor", "semester": 5},
    {"name": "Ian", "surname": "Mitchell", "degree": "Bachelor", "semester": 6},
    {"name": "Jill", "surname": "Perez", "degree": "Bachelor", "semester": 3},
    {"name": "Kyle", "surname": "Roberts", "degree": "Bachelor", "semester": 1},
    {"name": "Liam", "surname": "Turner", "degree": "Bachelor", "semester": 2},
    {"name": "Mona", "surname": "Phillips", "degree": "Bachelor", "semester": 4},
    {"name": "Nate", "surname": "Campbell", "degree": "Bachelor", "semester": 5},
    {"name": "Olivia", "surname": "Parker", "degree": "Bachelor", "semester": 6},
    {"name": "Pete", "surname": "Evans", "degree": "Bachelor", "semester": 3},
    {"name": "Quincy", "surname": "Edwards", "degree": "Bachelor", "semester": 1},
    {"name": "Rachel", "surname": "Collins", "degree": "Bachelor", "semester": 2},
    {"name": "Steve", "surname": "Stewart", "degree": "Bachelor", "semester": 4},
    {"name": "Tara", "surname": "Sanchez", "degree": "Bachelor", "semester": 5},
    {"name": "Ursula", "surname": "Morris", "degree": "Bachelor", "semester": 6},
    {"name": "Victor", "surname": "Rogers", "degree": "Bachelor", "semester": 3},
    {"name": "Wade", "surname": "Reed", "degree": "Bachelor", "semester": 1},
    {"name": "Xena", "surname": "Cook", "degree": "Bachelor", "semester": 2},
    {"name": "Yvonne", "surname": "Morgan", "degree": "Bachelor", "semester": 4},
    {"name": "Zach", "surname": "Bell", "degree": "Bachelor", "semester": 5},
    {"name": "Aaron", "surname": "Murphy", "degree": "Master", "semester": 1},
    {"name": "Betty", "surname": "Bailey", "degree": "Master", "semester": 2},
    {"name": "Carl", "surname": "Rivera", "degree": "Master", "semester": 3},
    {"name": "Diana", "surname": "Cooper", "degree": "Master", "semester": 4},
    {"name": "Ethan", "surname": "Richardson", "degree": "Master", "semester": 1},
    {"name": "Faye", "surname": "Cox", "degree": "Master", "semester": 2},
    {"name": "Gina", "surname": "Howard", "degree": "Master", "semester": 3},
    {"name": "Hugo", "surname": "Ward", "degree": "Master", "semester": 4},
    {"name": "Iris", "surname": "Torres", "degree": "Master", "semester": 1},
    {"name": "Jake", "surname": "Peterson", "degree": "Master", "semester": 2},
    {"name": "Kara", "surname": "Gray", "degree": "Master", "semester": 3},
    {"name": "Lana", "surname": "Ramirez", "degree": "Master", "semester": 4},
    {"name": "Mike", "surname": "James", "degree": "Master", "semester": 1},
    {"name": "Nora", "surname": "Watson", "degree": "Master", "semester": 2},
    {"name": "Omar", "surname": "Brooks", "degree": "Master", "semester": 3},
    {"name": "Paula", "surname": "Kelly", "degree": "Master", "semester": 4},
    {"name": "Quinn", "surname": "Sanders", "degree": "Master", "semester": 1},
    {"name": "Rita", "surname": "Price", "degree": "Master", "semester": 2},
    {"name": "Sean", "surname": "Bennett", "degree": "Master", "semester": 3},
    {"name": "Tina", "surname": "Wood", "degree": "Master", "semester": 4},
    {"name": "Uma", "surname": "Barnes", "degree": "Master", "semester": 1},
    {"name": "Vince", "surname": "Ross", "degree": "Master", "semester": 2},
    {"name": "Wendy", "surname": "Henderson", "degree": "Master", "semester": 3},
    {"name": "Xander", "surname": "Coleman", "degree": "Master", "semester": 4},
    {"name": "Yara", "surname": "Jenkins", "degree": "Master", "semester": 1},
    {"name": "Zane", "surname": "Perry", "degree": "Master", "semester": 2},
    {"name": "Amy", "surname": "Powell", "degree": "Master", "semester": 3},
    {"name": "Brian", "surname": "Long", "degree": "Master", "semester": 4},
    {"name": "Cathy", "surname": "Patterson", "degree": "Master", "semester": 1},
    {"name": "David", "surname": "Hughes", "degree": "Master", "semester": 2},
    {"name": "Ella", "surname": "Flores", "degree": "Master", "semester": 3},
    {"name": "Fiona", "surname": "Washington", "degree": "Master", "semester": 4},
    {"name": "George", "surname": "Butler", "degree": "Master", "semester": 1},
    {"name": "Holly", "surname": "Simmons", "degree": "Master", "semester": 2},
    {"name": "Ian", "surname": "Foster", "degree": "Master", "semester": 3},
    {"name": "Jill", "surname": "Gonzales", "degree": "Master", "semester": 4}
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
async def get_students_in_degree(degree_name: DegreeName, semester: int = 1):
    if degree_name is DegreeName.bachelor and semester > 6:
        return {"message": "Bachelor degree has only 6 semesters"}
    elif degree_name is DegreeName.master and semester > 4:
        return {"message": "Master degree has only 4 semesters"}

    filtered_students = filter(lambda student: student["degree"] == degree_name and student["semester"] == semester, fake_students_db)

    return list(filtered_students)
