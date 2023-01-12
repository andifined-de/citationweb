from pydantic import BaseModel, validator
import datetime
from datetime import date
from typing import Optional, ForwardRef
from .author import AuthorBase
from .tag import TagBase

import pandas as pd

LiteratureRead = ForwardRef('LiteratureRead')
LiteratureCreate = ForwardRef('LiteratureCreate')
LiteratureUpdate = ForwardRef('LiteratureUpdate')

class LiteratureBase(BaseModel):
	class Config:
		orm_mode = True

	@validator('published_date', pre=True, check_fields=False)
	def parse_published(cls, value):
		if (value != None):
			date = pd.to_datetime(value, errors='coerce').date()
			if (not pd.isnull(date)):
				return date
		return None

# FIXME: find better way to fix recursion
# maybe marshmallow as a layer?
#https://stackoverflow.com/questions/69544658/how-to-build-a-self-referencing-model-in-pydantic-with-dataclasses
class LiteratureReadReference(LiteratureBase):
	id: int
	# title: Optional[str]
	#doi: Optional[str]

class LiteratureRead(LiteratureBase):
	id: Optional[int]
	title: Optional[str]
	doi: Optional[str]
	sources: list[LiteratureReadReference] = list()

class LiteratureCreate(LiteratureBase):
	title: str
	subtitle: Optional[str]
	abstract: Optional[str]
	body: Optional[str]
	url: Optional[str]
	published_date: Optional[date]
	doi: Optional[str]
	sources: list['LiteratureBase'] = []
	authors: list[AuthorBase] = []
	tags: list[TagBase] = []

class LiteratureUpdate(LiteratureBase):
	id: int
	title: Optional[str]
	subtitle: Optional[str]
	abstract: Optional[str]
	body: Optional[str]
	url: Optional[str]
	published_date: Optional[date]
	doi: Optional[str]
	sources: list['LiteratureBase'] = []
	authors: list[AuthorBase] = []
	tags: list[TagBase] = []

class LiteratureDelete(LiteratureBase):
	id: int


LiteratureCreate.update_forward_refs()
LiteratureUpdate.update_forward_refs()
LiteratureRead.update_forward_refs()
