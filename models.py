from typing import List, Optional

from pydantic import BaseModel


class FileRequest(BaseModel):
    folder_id:str
    link: str
    name: str


class FolderRequest(BaseModel):
    course_id: str
    name: str
    files : Optional[List[str]] = None
    user_uid: str

class CourseRequest(BaseModel):
    day_week: str
    folder_id: Optional[List[str]] = None
    name: str
    user_uid: str