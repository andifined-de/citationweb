from sqlalchemy.orm import Session, aliased, joinedload

from domain.decorators.transaction import db
from domain.models.citation import CitationModel, FlatCitationModel
from domain.models.literature import LiteratureModel
from validation.response.citation import CitationResponse, LiteratureStump


@db
def get_all_citations(db: Session):
    result = db.query(FlatCitationModel).all()
    return list(map(lambda c: CitationResponse(
        cited=LiteratureStump(id=c.cited_id, title=c.cited_title,citation_score=1),
        citing=LiteratureStump(id=c.citing_id, title=c.citing_title, citation_score=1)
    ), result))
   #  return list(map(lambda c: CitationResponse.from_orm(c), result))
