from typing import List

from fastapi import APIRouter, HTTPException
from firebase_admin import firestore

from models.folderModels import FolderRequest, FolderResponse

db = None

router = APIRouter()

def removeFolder(course_id: str, folder_id: str):
        course_ref = db.collection('courses').document(course_id)
        courseDoc = course_ref.get()
        currentValue = courseDoc.to_dict().get('number_folder')
        currentFolder = courseDoc.to_dict().get('folders')
        currentFolder.remove(folder_id)
        new_value = currentValue - 1
        course_ref.update({'number_folder': new_value, 'folders': currentFolder})
        
def addFolder(course_id: str, folder_id: str):
        course_ref = db.collection('courses').document(course_id)
        courseDoc = course_ref.get()
        currentValue = courseDoc.to_dict().get('number_folder')
        currentFolder = courseDoc.to_dict().get('folders')
        currentFolder.append(folder_id)
        new_value = currentValue + 1
        course_ref.update({'number_folder': new_value, 'folders': currentFolder})

@router.get("/get-folders/{user_uid}/{course_id}", response_model=List[FolderResponse])
def get_folders(user_uid: str, course_id: str):
    global db
    if db is None:
        db = firestore.client()
    try:
        folders_ref = db.collection('folders')
        query = folders_ref.where("user_uid", "==", user_uid).where("course_id", "==", course_id)
        docs = query.stream()
        folders = []
        for doc in docs:
            folder = doc.to_dict()
            folder['id'] = doc.id
            folders.append(folder)
        return folders
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/delete-folder/{user_uid}/{course_id}/{folder_id}")
def delete_folder(user_uid:str, folder_id:str, course_id: str):
    global db
    if db is None:
        db = firestore.client()
    try:
        folder_ref = db.collection('folders').document(folder_id)
        folderDoc = folder_ref.get()
        
        if not folderDoc.exists:
            raise HTTPException(status_code=404, detail="Pasta não encontrada.")
        
        folder_data = folderDoc.to_dict()
        if folder_data['user_uid'] != user_uid:
            raise HTTPException(status_code=403, detail="Acesso negado. Você não tem permissão para excluir essa pasta.")
        removeFolder(course_id,folder_id)
        folder_ref.delete()
        return {"message": "Pasta excluída com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create-folder")
def create_folder(folder: FolderRequest):
    global db
    if db is None:
        db = firestore.client()
    try:
        doc_ref = db.collection('folders').add(folder.model_dump())
        addFolder(folder.course_id, doc_ref[1].id)
        return {"message": "Pasta criada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/update-folder/{user_uid}/{folder_id}")
def update_folder(user_uid: str, folder_id: str, new_name: str):
    global db
    if db is None:
        db = firestore.client()
    try:
        doc_ref = db.collection('folders').document(folder_id)
        doc = doc_ref.get()
        folder_data = doc.to_dict()
        
        if folder_data['user_uid'] != user_uid:
            raise HTTPException(status_code=403, detail="Acesso negado. Você não tem permissão para editar essa pasta.")
        
        update_data = {"name": new_name}
        doc_ref.update(update_data)
        return {"message": "Pasta atualizada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))