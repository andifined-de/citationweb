from pydantic import BaseModel
from typing import Optional


class AuthorResponse(BaseModel):
    id: int
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: str
    citation_score: int

    class Config:
        orm_mode = True
