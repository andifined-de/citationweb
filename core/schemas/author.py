from pydantic import BaseModel
from .email import EmailCreate, EmailBase
from typing import Optional

class AuthorBase(BaseModel):
	class Config:
		orm_mode = True

class AuthorCreate(AuthorBase):
	emails: list[EmailCreate] = []  # EmailCreate, because new authors cannot have existing emails
	first_name: str
	last_name: str
	orcid: Optional[str]

class AuthorUpdate(AuthorBase):
	id: int
	emails: list[EmailBase] = []
	first_name: Optional[str]
	last_name: Optional[str]
	orcid: Optional[str]

class AuthorDelete(AuthorBase):
	id: int
