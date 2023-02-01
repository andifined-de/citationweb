from pydantic import BaseModel
from .email import EmailCreate, EmailBase
from typing import Optional
from dataclasses import dataclass
from typing import Protocol


class AuthorInput(Protocol):
    id: Optional[int]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    emails: list[str] = []
    orcid: Optional[str]


class AuthorData(BaseModel):
    id: int
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: str
    full_name: str
    orcid: Optional[str]
    emails: Optional[list[str]]
