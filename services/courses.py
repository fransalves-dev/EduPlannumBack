from typing import List

from fastapi import APIRouter, HTTPException
from firebase_admin import firestore

from models.courseModels import CourseRequest, CourseResponse

db = None

router = APIRouter()

@router.get("/get-courses/{user_uid}", response_model=List[CourseResponse])
def get_courses(user_uid: str):
    global db
    if db is None:
        db = firestore.client()
    try:
        courses_ref = db.collection('courses')
        query = courses_ref.where("user_uid", "==", user_uid)
        docs = query.stream()
        courses = []
        for doc in docs:
            course = doc.to_dict()
            course['id'] = doc.id
            courses.append(course)
        return courses
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/delete-course/{user_uid}&{course_id}")
def delete_course(user_uid:str, course_id: str):
    global db
    if db is None:
        db = firestore.client()
    try:
        doc_ref = db.collection('courses').document(course_id)
        doc = doc_ref.get()
        
        course_data = doc.to_dict()
        if course_data['user_uid'] != user_uid:
            raise HTTPException(status_code=403, detail="Acesso negado. Você não tem permissão para excluir essa matéria.")
        
        doc_ref.delete()
        return {"message": "Matéria excluída com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create-course")
def create_course(course: CourseRequest):
    global db
    if db is None:
        db = firestore.client()
    try:
        doc_ref = db.collection('courses').add(course.model_dump())
        return {"message": "Matéria criada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/update-course/{user_uid}&{course_id}")
def update_course(user_uid: str, course_id: str, new_name: str, new_day: str):
    global db
    if db is None:
        db = firestore.client()
    try:
        doc_ref = db.collection('courses').document(course_id)
        doc = doc_ref.get()
        course_data = doc.to_dict()
        
        if course_data['user_uid'] != user_uid:
            raise HTTPException(status_code=403, detail="Acesso negado. Você não tem permissão para excluir essa matéria.")
        
        update_data = {"name": new_name , "day_week": new_day}
        doc_ref.update(update_data)
        return {"message": "Curso atualizado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))