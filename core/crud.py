from sqlalchemy.orm import Session, aliased
import models
from schemas.address import AddressCreate
from schemas.author import AuthorCreate
from schemas.literature import *

def create_address(db: Session, address: AddressCreate):
	db.add(address)
	db.commit()
	db.refresh(address)

def create_author(db: Session, author: AuthorCreate):
	created_author = db.add(models.Author(
		first_name = author.first_name,
		last_name = author.last_name,
		orcid = author.orcid
	))
	for email in author.emails:
		db.add(models.Email(name = email.name, author_id = created_author.id))
	return created_author


def create_update_literature(db: Session, literature: LiteratureBase):
	result = get_literature(db, literature)
	if (result == None):
		result = create_literature(db, literature)

	return result

def create_literature(db: Session, literature: LiteratureCreate):
	created_literature = db.add(models.Literature(
		title = literature.title,
		subtitle = literature.subtitle,
		abstract = literature.abstract,
		body = literature.body,
		url = literature.url,
		published_date = literature.published_date,
		doi = literature.doi
	))
	for author in literature.authors:
		result = create_author(db, author)
		created_literature.authors.add(result)
	for source in literature.sources:
		# if literature is already in database, link them, if not, create them and update later when supplied
		result = create_update_literature(db, source)
		created_literature.sources.add(result)
	return created_literature

def get_literature (db: Session, literature: LiteratureRead):
	if (hasattr(literature, 'id') and literature.id != None):
		return db.query(models.Literature).get(literature.id)
	if (literature.doi != None):
		return db.query(models.Literature).filter(models.Literature.doi == literature.doi).first()
	if (literature.title != None):
		return db.query(models.Literature).filter(models.Literature.title == literature.title).first()

def get_all_literature(db: Session):
	return db.query(models.Literature).all()

def get_all_citations(db: Session):
	source_literature = aliased(models.Literature)
	referencing_literature = aliased(models.Literature)
	result = db.query(models.Citation).join(
		source_literature, models.Citation.source_id == source_literature.id
	).join(
		referencing_literature, models.Citation.referencing_id == referencing_literature.id
	).all()
	return result
