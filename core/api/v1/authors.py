from fastapi import APIRouter

from validation.response.author import AuthorResponse
from services import author as author_service

author_router = APIRouter()


@author_router.get('/', response_model=list[AuthorResponse])
async def get_citation_network():
    return author_service.get_all_author_citations()
