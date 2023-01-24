import crud
from database.transaction import Transaction
from models import Author
from validation.response.citation import AuthorCitationResponse
from fastapi import Depends


def get_author_citations(author: Author):  # TODO: probably very! slow!
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


def get_all_author_citations(tx: Transaction = Depends(Transaction)):
    all_authors = crud.get_all_authors(tx.session)
    citations: list[AuthorCitationResponse] = []
    for author in all_authors:
        citations.extend(get_author_citations(author))
    return citations


