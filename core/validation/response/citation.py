from pydantic import BaseModel
from typing import Optional
from validation.response.literature import LiteratureResponse


class LiteratureStump(BaseModel):
	id: int
	title: str
	citation_score: int

	class Config:
		orm_mode = True


class CitationResponse(BaseModel):
	id: int
	cited: LiteratureStump
	citing: LiteratureStump

	class Config:
		orm_mode = True


class AuthorCitationResponse(BaseModel):
	cited_name: str
	cited_id: int
	citing_name: str
	citing_id: int
	weight: int
