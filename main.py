import firebase_admin
from fastapi import FastAPI
from firebase_admin import credentials

from services.courses import router as courses_router
from services.files import router as files_router
from services.folders import router as folders_router
from services.reminders import router as reminders_router

app = FastAPI()

cred = credentials.Certificate("./Firebase/eduplanum-tcc-firebase-adminsdk-npm7k-f9a3e7f47d.json")
firebase_admin.initialize_app(cred)

app.include_router(courses_router)
app.include_router(folders_router)
app.include_router(files_router)
app.include_router(reminders_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)