from fastapi import APIRouter, HTTPException
from firebase_admin import firestore

from models import CourseRequest

db = None

router = APIRouter()

@router.get("/get-courses")
def get_courses():
    global db
    if db is None:
        db = firestore.client()
    try:
        courses_ref = db.collection('courses')
        docs = courses_ref.stream()
        courses = [doc.to_dict() for doc in docs]
        return courses
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create-course")
def create_course(course: CourseRequest):
    global db
    if db is None:
        db = firestore.client()
    try:
        doc_ref = db.collection('courses').add(course.model_dump())
        return {"message": "Curso criado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/update-course/{course_id}")
def update_course(course_id: str, course: CourseRequest):
    global db
    if db is None:
        db = firestore.client()
    try:
        doc_ref = db.collection('courses').document(course_id)
        doc_ref.update(course.model_dump())
        return {"message": "Curso atualizado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/delete-course/{course_id}")
def delete_course(course_id: str):
    global db
    if db is None:
        db = firestore.client()
    try:
        doc_ref = db.collection('courses').document(course_id)
        doc_ref.delete()
        return {"message": "Curso excluído com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))