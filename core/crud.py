
"""
from sqlalchemy.orm import Session, aliased, joinedload
import models
from validation.request.literature import CreateLiteratureRequest, SearchLiteratureRequest
from schemas.address import AddressCreate
from schemas.author import AuthorCreate
from schemas.literature import *
from validation.request.author import SearchAuthorRequest, CreateAuthorRequest
import time



def create_address(db: Session, address: AddressCreate):
    db.add(address)
    db.commit()
    db.refresh(address)


def get_author(db: Session, author: SearchAuthorRequest):
    if hasattr(author, 'id') and author.id is not None:
        return db.query(models.Author).get(author.id)
    if author.orcid is not None:
        return db.query(models.Author).filter(models.Author.orcid == author.orcid).first()
    if len(author.emails) > 0:
        for email in author.emails:
            result = db.query(models.Author).filter(models.Author.emails.any(text=email)).first()
            if result is not None:
                return result
    if author.last_name is not None and author.first_name is not None:
        return db.query(models.Author).filter(models.Author.first_name == author.first_name).filter(
            models.Author.last_name == author.last_name).first()


def create_author(db: Session, author: CreateAuthorRequest | SearchAuthorRequest):
    created_author = models.Author(
        first_name=author.first_name,
        last_name=author.last_name,
        orcid=author.orcid
    )
    db.add(created_author)
    for email in author.emails:
        email_model = models.Email(text=email, author_id=created_author.id)
        db.add(email_model)
        db.commit()
        db.refresh(email_model)
        created_author.emails.append(email_model)
    db.commit()
    db.refresh(created_author)
    return created_author


def create_update_author(db: Session, author: SearchAuthorRequest | CreateAuthorRequest):
    result = get_author(db, author)
    if result is None:
        result = create_author(db, author)  # authorcreate and SearchAuthorRequest are incompatible
    return result


def create_update_literature(db: Session, literature: CreateLiteratureRequest | SearchLiteratureRequest):
    result = get_literature(db, literature)
    if result is None:
        result = create_literature(db, literature)

    return result


def create_literature(db: Session, literature: CreateLiteratureRequest):
    created_literature = models.Literature(
        title=literature.title,
        subtitle=literature.subtitle,
        abstract=literature.abstract,
        body=literature.body,
        url=literature.url,
        published_date=literature.published_date,
        doi=literature.doi
    )
    db.add(created_literature)
    for author in literature.authors:
        if author.first_name is None or author.last_name is None:
            continue
        result = create_update_author(db, author)
        created_literature.authors.append(result)
    for citation in literature.citations:
        # if literature is already in domain, link them, if not, create them and update later when supplied
        result = create_update_literature(db, citation)
        created_literature.citations.append(result)
    db.commit()
    db.refresh(created_literature)
    return created_literature


def get_literature(db: Session, literature: SearchLiteratureRequest):
    if hasattr(literature, 'id') and literature.id is not None:
        return db.query(models.Literature).get(literature.id)
    if literature.doi is not None:
        return db.query(models.Literature).filter(models.Literature.doi == literature.doi).first()
    if literature.title is not None and literature.title != '':
        return db.query(models.Literature).filter(models.Literature.title == literature.title).first()


def get_all_literature(db: Session):
    return db.query(models.Literature).all()


# Anfragen aller Zitationen, die Literatur als Quelle haben, dann darüber anfragen des Datums dieser Literatur.
# Durchschnitt des Datums bilden (Ausreißer?) und diesen in Relation bringen mit aktuellem Jahr / neuester Literatur

def get_all_citations(db: Session):
    source_literature = aliased(models.Literature)
    referencing_literature = aliased(models.Literature)
    result = db.query(models.Citation).options(joinedload("source_literature,referencing_literature")).join(
        source_literature, models.Citation.cited_id == source_literature.id
    ).join(
        referencing_literature, models.Citation.citing_id == referencing_literature.id
    ).all()
    return result


def get_all_authors(db: Session):
    return db.query(models.Author).all()
"""
