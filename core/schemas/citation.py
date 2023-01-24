from pydantic import BaseModel
from typing import Optional
from schemas.literature import LiteratureRead

class CitationBase(BaseModel):
	class Config:
		orm_mode = True

class CitationLiteratureRead(BaseModel):
	id: int
	title: Optional[str]
	citation_score: Optional[int]

	class Config:
		orm_mode = True

class CitationRead(CitationBase):
	page_start: Optional[str]
	page_end: Optional[str]
	cited: CitationLiteratureRead
	citing: CitationLiteratureRead
