from pydantic import BaseModel, validator
import pandas as pd
from typing import Optional
from validation.request.author import CreateAuthorRequest, UpdateAuthorRequest, ReadAuthorRequest, \
    SearchAuthorRequest
from datetime import date


class ReadLiteratureRequest(BaseModel):
    id: int


class SearchLiteratureRequest(BaseModel):
    id: Optional[int]
    title: Optional[str]
    doi: Optional[str]


class CreateLiteratureRequest(BaseModel):
    title: str
    subtitle: Optional[str]
    abstract: Optional[str]
    body: Optional[str]
    url: Optional[str]
    authors: list[CreateAuthorRequest | SearchAuthorRequest] = []
    doi: Optional[str]
    citations: list['CreateLiteratureRequest'] = []
    published_date: Optional[date]

    @validator('published_date', pre=True, check_fields=False)
    def parse_published(cls, value):
        if value is not None:
            d = pd.to_datetime(value, errors='coerce').date()
            if not pd.isnull(d):
                return d
        return None


class UpdateLiteratureRequest(BaseModel):
    id: int
    title: Optional[str]
    subtitle: Optional[str]
    authors: list[CreateAuthorRequest | SearchAuthorRequest] = []
    doi: Optional[str]
    abstract: Optional[str]
    body: Optional[str]
    url: Optional[str]
    citations: list[CreateLiteratureRequest | ReadLiteratureRequest] = []
    published_date: Optional[date]

    @validator('published_date', pre=True, check_fields=False)
    def parse_published(cls, value):
        if value is not None:
            d = pd.to_datetime(value, errors='coerce').date()
            if not pd.isnull(d):
                return d
        return None


class DeleteAuthorRequest(BaseModel):
    id: int
