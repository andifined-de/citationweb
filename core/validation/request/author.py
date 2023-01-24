from pydantic import BaseModel
from typing import Optional


class CreateAuthorRequest(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: str
    emails: list[str] = []
    orcid: Optional[str]


class ReadAuthorRequest(BaseModel):
    id: int


class UpdateAuthorRequest(BaseModel):
    id: int
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    emails: list[str] = []


class DeleteAuthorRequest(BaseModel):
    id: int


class SearchAuthorRequest(BaseModel):
    id: Optional[int]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    emails: list[str] = []
    orcid: Optional[str]
