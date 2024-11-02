from typing import List

from fastapi import APIRouter, HTTPException
from firebase_admin import firestore

from models.fileModels import FileRequest, FileResponse

db = None

router = APIRouter()

def removeFile(folder_id: str, file_id: str):
        folder_ref = db.collection('folders').document(folder_id)
        folderDoc = folder_ref.get()
        currentValue = folderDoc.to_dict().get('number_file')
        currentFile = folderDoc.to_dict().get('files')
        currentFile.remove(file_id)
        new_value = currentValue - 1
        folder_ref.update({'number_file': new_value, 'files': currentFile})
        
def addFile(folder_id: str, file_id: str):
        folder_ref = db.collection('folders').document(folder_id)
        folderDoc = folder_ref.get()
        currentValue = folderDoc.to_dict().get('number_file')
        currentFile = folderDoc.to_dict().get('files')
        currentFile.append(file_id)
        new_value = currentValue + 1
        folder_ref.update({'number_file': new_value, 'files': currentFile})

@router.get("/get-files/{user_uid}&{folder_id}", response_model=List[FileResponse])
def get_files(user_uid: str, folder_id: str):
    global db
    if db is None:
        db = firestore.client()
    try:
        files_ref = db.collection('files')
        query = files_ref.where("user_uid", "==", user_uid).where("folder_id", "==", folder_id)
        docs = query.stream()
        files = []
        for doc in docs:
            file = doc.to_dict()
            file['id'] = doc.id
            files.append(file)
        return files
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/delete-file/{user_uid}/{file_id}/{folder_id}")
def delete_file(user_uid:str, file_id:str, folder_id: str):
    global db
    if db is None:
        db = firestore.client()
    try:
        file_ref = db.collection('files').document(file_id)
        fileDoc = file_ref.get()
        
        file_data = fileDoc.to_dict()
        if file_data['user_uid'] != user_uid:
            raise HTTPException(status_code=403, detail="Acesso negado. Você não tem permissão para excluir essa pasta.")
        removeFile(folder_id, file_id)
        file_ref.delete()
        return {"message": "Arquivo excluído com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create-file")
def create_file(file: FileRequest):
    global db
    if db is None:
        db = firestore.client()
    try:
        doc_ref = db.collection('files').add(file.model_dump())
        addFile(file.folder_id, doc_ref[1].id)
        return {"message": "Arquivo criado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))