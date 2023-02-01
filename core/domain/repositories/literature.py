from typing import Protocol, Optional

from sqlalchemy.orm import Session

from database.decorators.transaction import db
from database.models.author import AuthorModel, EmailModel
from database.models.literature import LiteratureModel


@db
def save_literature(literature: LiteratureModel, db: Session) -> LiteratureModel:
    db.add(literature)
    db.flush()
    return literature


@db
def get_literature(id_: int, db: Session) -> LiteratureModel:
    return db.query(LiteratureModel).get(id_)


@db
def find_literature_by_title(title: str, db: Session) -> Optional[LiteratureModel]:
    return db.query(LiteratureModel).filter(LiteratureModel.title == title).first()


@db
def find_literature_by_doi(doi: str, db: Session) -> Optional[LiteratureModel]:
    return db.query(LiteratureModel).filter(LiteratureModel.doi == doi).first()

