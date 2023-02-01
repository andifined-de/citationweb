from pydantic import BaseModel
from typing import Optional, Protocol

from schemas.author import AuthorInput, AuthorData


class LiteratureInput(Protocol):
	id: Optional[int]
	title: Optional[str]
	subtitle: Optional[str]
	doi: Optional[str]
	url: Optional[str]
	citations: list['LiteratureInput'] = []
	authors: list[AuthorInput] = []


# FIXME: find better way to fix recursion
# maybe marshmallow as a layer?
# https://stackoverflow.com/questions/69544658/how-to-build-a-self-referencing-model-in-pydantic-with-dataclasses
class LiteratureReferenceData(BaseModel):
	id: int
	title: str
	doi: Optional[str]
	citation_score: Optional[int] = None
	date_score: Optional[float] = None

	class Config:
		orm_mode = True


class LiteratureData(BaseModel):
	id: Optional[int]
	title: str
	doi: Optional[str]
	citations: list[LiteratureReferenceData] = []
	authors: list[AuthorData] = []
	citation_score: Optional[int] = None
	date_score: Optional[float] = None

	class Config:
		orm_mode = True



