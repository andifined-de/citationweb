from sqlalchemy.orm import Session, aliased, joinedload

from database.decorators.transaction import db
from database.models.citation import CitationModel
from database.models.literature import LiteratureModel
from validation.response.citation import CitationResponse


@db
def get_all_citations(db: Session):
    source_literature = aliased(LiteratureModel)
    referencing_literature = aliased(LiteratureModel)
    result = db.query(CitationModel).all()
    return list(map(lambda c: CitationResponse.from_orm(c), result))
