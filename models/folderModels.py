from typing import List, Optional

from pydantic import BaseModel


class FolderRequest(BaseModel):
    name: str
    course_id: str
    course_name: str
    files: Optional[List[str]] = None
    todo: Optional[List[str]] = None
    number_file: int
    number_todo: int
    user_uid: str

class FolderResponse(BaseModel):
    id: str
    name: str
    course_id: str
    course_name: str
    files: Optional[List[str]] = None
    todo: Optional[List[str]] = None
    number_file: int
    number_todo: int
    user_uid: str