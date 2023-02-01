from typing import Optional

from domain.decorators.transaction import transactional
from domain.models.author import AuthorModel, EmailModel
from domain.transaction import Transaction
from schemas.author import AuthorInput

from validation.request.author import CreateAuthorRequest, SearchAuthorRequest
from validation.response.citation import AuthorCitationResponse
from fastapi import Depends

from domain.repositories import author as repository


@transactional
def get_create_author(request: AuthorInput) -> AuthorModel:
    author: Optional[AuthorModel] = None
    # try to get author by different means
    if hasattr(request, 'id') and request.id is not None:
        return repository.get_author(id)
    if author is None and request.orcid is not None:
        author = repository.find_author_by_orcid(request.orcid)
    if author is None and request.first_name is not None and request.last_name is not None:
        author = repository.find_author_by_name(request.first_name, request.middle_name, request.last_name)
    # no author found, create a new one
    if author is None:
        author = repository.save_author(AuthorModel(
            first_name=request.first_name,
            middle_name=request.middle_name,
            last_name=request.last_name,
            orcid=request.orcid
        ))
        emails = list(map(lambda e: EmailModel(text=e, author_id=author.id), request.emails))
        repository.save_emails(emails, author)
    return author


@transactional
def get_all_authors() -> list[AuthorModel]:
    return repository.get_all_authors()


def get_author_citations(author: AuthorModel):  # TODO: probably very! slow!
    citations = {}
    for literature in author.literature:  # up to 100?
        for citation in literature.citations:  # up to 100?
            for a in citation.authors:  # up to 5?
                key = f'{author.id},{a.id}'
                if key not in citations:
                    citations[key] = AuthorCitationResponse(
                        citing_id=author.id,
                        cited_id=a.id,
                        citing_name=author.full_name,
                        cited_name=a.full_name,
                        weight=1
                    )
                else:
                    citations[key] = AuthorCitationResponse(
                        citing_id=author.id,
                        cited_id=a.id,
                        citing_name=author.full_name,
                        cited_name=a.full_name,
                        weight=citations[key].weight + 1
                    )
    return citations.values()


@transactional
def get_all_author_citations():
    citations: list[AuthorCitationResponse] = []
    for author in get_all_authors():
        citations.extend(get_author_citations(author))
    return citations
