from fastapi import APIRouter, HTTPException
from firebase_admin import firestore

from models import FolderRequest

db = None

router = APIRouter()

@router.get("/get-folders")
def get_courses():
    global db
    if db is None:
        db = firestore.client()
    try:
        folders_ref = db.collection('folders')
        docs = folders_ref.stream()
        folders = [doc.to_dict() for doc in docs]
        return folders
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create-folder")
def create_course(folder: FolderRequest):
    global db
    if db is None:
        db = firestore.client()
    try:
        doc_ref = db.collection('folders').add(folder.model_dump())
        return {"message": "Pasta criada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/update-folder/{folder_id}")
def update_course(folder_id: str, folder: FolderRequest):
    global db
    if db is None:
        db = firestore.client()
    try:
        doc_ref = db.collection('folders').document(folder_id)
        doc_ref.update(folder.model_dump())
        return {"message": "Pasta atualizada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/delete-course/{folder_id}")
def delete_course(folder_id: str):
    global db
    if db is None:
        db = firestore.client()
    try:
        doc_ref = db.collection('folders').document(folder_id)
        doc_ref.delete()
        return {"message": "Pasta excluída com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))