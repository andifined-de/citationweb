from domain.decorators.transaction import transactional
from domain.models.citation import CitationModel

from domain.repositories import citation as repository
from validation.response.citation import CitationResponse
import time


@transactional
def get_all_citations() -> list[CitationResponse]:
    t = time.time()
    result = repository.get_all_citations()
    print(f'got results in {time.time() - t} seconds')
    return result


@transactional
def search(search_query: str):
    return repository.search(search_query, 1)
