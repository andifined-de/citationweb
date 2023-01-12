from pydantic import BaseModel
from typing import Optional
from schemas.literature import LiteratureRead

class CitationBase(BaseModel):
	class Config:
		orm_mode = True

class CitationLiteratureRead(BaseModel):
	id: int
	title: Optional[str]

	class Config:
		orm_mode = True

class CitationRead(CitationBase):
	source_id: int
	referencing_id: int
	page_start: Optional[str]
	page_end: Optional[str]
	source: CitationLiteratureRead
	referencing_paper: CitationLiteratureRead
