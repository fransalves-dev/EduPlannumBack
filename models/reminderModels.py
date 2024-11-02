from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ReminderRequest(BaseModel):
    name: str
    course_id: str
    course_name: str
    folder_id: str
    folder_name: str
    file_id: str
    file_name: str
    timeReminder: datetime
    message: str
    user_uid: str

class ReminderResponse(BaseModel):
    id: str
    name: str
    course_id: str
    course_name: str
    folder_id: str
    folder_name: str
    file_id: str
    file_name: str
    timeReminder: datetime
    message: str
    user_uid: str