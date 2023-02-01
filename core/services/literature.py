from typing import Optional

from domain.decorators.transaction import transactional
from domain.models.literature import LiteratureModel
from validation.request.literature import CreateLiteratureRequest, SearchLiteratureRequest

from domain.repositories import literature as repository
from services.author import get_create_author


@transactional
def get_create_literature(request: CreateLiteratureRequest | SearchLiteratureRequest) -> LiteratureModel:
    literature: Optional[LiteratureModel] = None
    if hasattr(request, 'id') and request.id is not None:
        return repository.get_literature(id)
    if request.doi is not None:
        literature = repository.find_literature_by_doi(request.doi)
    if literature is None and request.title is not None and request.title != '':
        literature = repository.find_literature_by_title(request.title)
    if literature is None:
        authors = list(map(lambda a: get_create_author(a), request.authors))
        cited_literature = list(map(lambda c: get_create_literature(c), request.citations))
        literature = repository.save_literature(LiteratureModel(
            doi=request.doi,
            title=request.title,
            subtitle=request.subtitle,
            # abstract=request.abstract,
            # body=request.body,
            url=request.url,
            published_date=request.published_date,
            authors=authors,
            citations=cited_literature
        ))
    return literature
