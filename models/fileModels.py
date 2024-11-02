from typing import List, Optional

from pydantic import BaseModel


class FileRequest(BaseModel):
    name: str
    folder_id: str
    folder_name: str
    type: str
    typeLocation: str
    link: Optional[str] = None
    id_storage: Optional[str] = None
    user_uid: str

class FileResponse(BaseModel):
    id: str
    name: str
    folder_id: str
    folder_name: str
    type: str
    typeLocation: str
    link: Optional[str] = None
    id_storage: Optional[str] = None
    user_uid: str
