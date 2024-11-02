from typing import List, Optional

from pydantic import BaseModel


class CourseRequest(BaseModel):
    name: str
    day_week: str
    folders: Optional[List[str]] = None
    reminders: Optional[List[str]] = None
    number_folder: int
    number_reminder: int
    user_uid: str

class CourseResponse(BaseModel):
    id: str
    name: str
    day_week: str
    folders: Optional[List[str]] = None
    reminders: Optional[List[str]] = None
    number_folder: int
    number_reminder: int
    user_uid: str