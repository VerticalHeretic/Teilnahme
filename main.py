from fastapi import FastAPI
from enum import Enum

class ClassName(str, Enum):
    son = "Specjalistyczne Oprogramowanie Narzędziowe"
    dpp = "Dobre Praktyki Programowania"

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int):
    return {"user_id": user_id}

@app.get("/classes/{class_name}")
async def get_class(class_name: ClassName):
    if class_name is ClassName.son:
        return {"model_name": class_name, "message": "Licencjat for the win!"}
    elif class_name is ClassName.dpp:
        return {"model_name": class_name, "message": "Magisterka for the win!"}

    return  {"model_name": class_name, "message": "No win for you :("}
