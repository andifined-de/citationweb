from typing import Protocol, Optional

from sqlalchemy.orm import Session

from database.decorators.transaction import db
from database.models.author import AuthorModel, EmailModel


@db
def save_author(author: AuthorModel, db: Session) -> AuthorModel:
    db.add(author)
    db.flush()
    return author


@db
def save_emails(emails: list[EmailModel], author: AuthorModel, db: Session) -> AuthorModel:
    db.add_all(emails)
    db.flush()
    author.emails.extend(emails)
    db.flush()
    return author


@db
def get_author(id_: int, db: Session) -> AuthorModel:
    return db.query(AuthorModel).get(id_)


@db
def get_all_authors(db: Session) -> list[AuthorModel]:
    return db.query(AuthorModel).all()


@db
def find_author_by_name(first_name: str, middle_name: Optional[str], last_name: str, db: Session) -> Optional[AuthorModel]:
    query = db.query(AuthorModel).filter(
        AuthorModel.first_name == first_name
    ).filter(
        AuthorModel.last_name == last_name
    )
    if middle_name is not None:
        query = query.filter(
            AuthorModel.middle_name == middle_name
        )
    return query.first()


@db
def find_author_by_orcid(orcid: str, db: Session) -> Optional[AuthorModel]:
    return db.query(AuthorModel).filter(AuthorModel.orcid == orcid).first()


@db
def find_author_by_email(email: str, db: Session) -> Optional[AuthorModel]:
    return db.query(AuthorModel).filter(AuthorModel.emails.any(EmailModel.text == email)).first()
