from pydantic import BaseModel
from typing import Optional
from validation.response.literature import LiteratureResponse
from dataclasses import dataclass

class LiteratureStump(BaseModel):
	id: int
	title: str
	citation_score: int

	class Config:
		orm_mode = True


@dataclass
class CitationLiteratureData:
	id: int
	title: str
	citation_score: int


@dataclass
class CitationData:
	id: int
	cited: CitationLiteratureData
	citing: CitationLiteratureData


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
