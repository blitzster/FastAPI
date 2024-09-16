from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


students = {
    1: {
        "name": "John",
        "age": 20,
        "grade": "A"
    }
}

class Student(BaseModel):
    name: str
    age: int
    grade: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None

@app.get("/")
def index():
    return {"name": "First Data"}

# Path Parameter
@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(description="The ID of the student you want to view", gt=0, lt=3)):
    return students[student_id]

#Query Parameter
@app.get("/get-by-name")
def get_student(name: str = None):  #str = None will remove the required option from the page
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not Found"}


#POST
@app.post("/create-student/{student_id}")
def create_student(student_id: int, student:Student):
    if student_id in students:
        return {"Error":"Student exists"}
    students[student_id] = student
    return students[student_id]

#PUT
@app.put("/update-student/{student_id}")
def update_student(student_id: int, student:UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist."}
    
    if student.name != None:
        students[student_id].name = student.name

    if student.age != None:
        students[student_id].age = student.age
    
    if student.grade != None:
        students[student_id].grade = student.grade
    
    return students[student_id]

#DELETE
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}

    del students[student_id]
    return {"Message": "Student deleted successfully"}