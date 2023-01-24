from pydantic import BaseModel
from typing import Optional
from validation.response.author import AuthorResponse


class LiteratureResponse(BaseModel):
	id: int
	title: Optional[str]
	subtitle: Optional[str]
	authors: list[AuthorResponse] = []
	doi: Optional[str]
	citations: list['LiteratureResponse'] = []

	class Config:
		orm_mode = True
