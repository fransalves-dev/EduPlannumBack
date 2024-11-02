from typing import List

from fastapi import APIRouter, HTTPException
from firebase_admin import firestore

from models.reminderModels import ReminderRequest, ReminderResponse

db = None

router = APIRouter()

def removeReminder(course_id: str, reminder_id: str):
        course_ref = db.collection('courses').document(course_id)
        courseDoc = course_ref.get()
        currentValue = courseDoc.to_dict().get('number_reminder')
        currentReminder = courseDoc.to_dict().get('reminders')
        currentReminder.remove(reminder_id)
        new_value = currentValue - 1
        course_ref.update({'number_reminder': new_value, 'reminders': currentReminder})
        
def addReminder(course_id: str, reminder_id: str):
        course_ref = db.collection('courses').document(course_id)
        courseDoc = course_ref.get()
        currentValue = courseDoc.to_dict().get('number_reminder')
        currentReminder = courseDoc.to_dict().get('reminders')
        currentReminder.append(reminder_id)
        new_value = currentValue + 1
        course_ref.update({'number_reminder': new_value, 'reminders': currentReminder})

@router.get("/get-reminders/{user_uid}&{course_id}", response_model=List[ReminderResponse])
def get_reminders(user_uid: str, course_id: str):
    global db
    if db is None:
        db = firestore.client()
    try:
        reminder_ref = db.collection('reminders')
        query = reminder_ref.where("user_uid", "==", user_uid).where("course_id", "==", course_id)
        docs = query.stream()
        reminders = []
        for doc in docs:
            reminder = doc.to_dict()
            reminder['id'] = doc.id
            reminders.append(reminder)
        return reminders
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/delete-reminder/{user_uid}/{reminder_id}/{course_id}")
def delete_reminder(user_uid:str, reminder_id:str, course_id: str):
    global db
    if db is None:
        db = firestore.client()
    try:
        reminder_ref = db.collection('reminders').document(reminder_id)
        reminderDoc = reminder_ref.get()
        
        reminder_data = reminderDoc.to_dict()
        if reminder_data['user_uid'] != user_uid:
            raise HTTPException(status_code=403, detail="Acesso negado. Você não tem permissão para excluir esse lembrete.")
        removeReminder(course_id,reminder_id)
        reminder_ref.delete()
        return {"message": "Lembrete excluído com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create-reminder")
def create_reminder(reminder: ReminderRequest):
    global db
    if db is None:
        db = firestore.client()
    try:
        doc_ref = db.collection('reminders').add(reminder.model_dump())
        addReminder(reminder.course_id, doc_ref[1].id)
        return {"message": "Lembrete criado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/update-reminder/{user_uid}&{reminder_id}")
def update_reminder(user_uid: str, reminder_id: str, new_message: str):
    global db
    if db is None:
        db = firestore.client()
    try:
        doc_ref = db.collection('reminders').document(reminder_id)
        doc = doc_ref.get()
        reminder_data = doc.to_dict()
        
        if reminder_data['user_uid'] != user_uid:
            raise HTTPException(status_code=403, detail="Acesso negado. Você não tem permissão para atualizar esse lembrete.")
        
        update_data = {"message": new_message}
        doc_ref.update(update_data)
        return {"message": "Lembrete atualizado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))