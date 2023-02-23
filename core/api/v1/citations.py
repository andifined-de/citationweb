from fastapi import APIRouter
from validation.response.citation import CitationResponse
from services import citation as citation_service


citation_router = APIRouter()


@citation_router.get('/', response_model=list[CitationResponse])
async def get_citation_network():
    return citation_service.get_all_citations()

@citation_router.get('/search', response_model=list[CitationResponse])
async def search_citations(q: str):
    return citation_service.search(q)
