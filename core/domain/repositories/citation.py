from sqlalchemy.orm import Session, aliased, joinedload

from domain.decorators.transaction import db
from domain.models.citation import CitationModel
from domain.models.literature import LiteratureModel
from validation.response.citation import CitationResponse


@db
def get_all_citations(db: Session):
    result = db.query(CitationModel).options(
        joinedload(CitationModel.citing),
        joinedload(CitationModel.cited)
    ).all()
    return list(map(lambda c: CitationResponse.from_orm(c), result))
   #  return list(map(lambda c: CitationResponse.from_orm(c), result))
