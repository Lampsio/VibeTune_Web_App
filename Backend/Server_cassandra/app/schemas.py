from pydantic import BaseModel, Field
from ulid import ULID

class SubtitleCreate(BaseModel):
    id_music: str
    start: int
    end: int
    text: str = Field(..., max_length=100)

class SubtitleResponse(BaseModel):
    id: str
    id_music: str
    start: int
    end: int
    text: str
