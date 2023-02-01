from pydantic import BaseModel
from typing import Optional
from schemas.literature import LiteratureReferenceData


class CitationData(BaseModel):
	id: int
	page_start: Optional[str]
	page_end: Optional[str]
	cited: LiteratureReferenceData
	citing: LiteratureReferenceData

	class Config:
		orm_mode = True

