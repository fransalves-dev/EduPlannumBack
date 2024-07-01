import firebase_admin
from fastapi import FastAPI, HTTPException
from firebase_admin import credentials, firestore

from services.courses import router as courses_router
from services.folders import router as folders_router

app = FastAPI()

cred = credentials.Certificate("./Firebase/eduplanum-tcc-firebase-adminsdk-npm7k-f9a3e7f47d.json")
firebase_admin.initialize_app(cred)

app.include_router(courses_router)
app.include_router(folders_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)