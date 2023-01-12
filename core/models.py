from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, UnicodeText
from sqlalchemy.orm import relationship, deferred
from database import Base


tag_literature_rel = Table(
	'tag_literature',
	Base.metadata,
	Column('tag_id', Integer, ForeignKey('tags.id')),
	Column('literature_id', Integer, ForeignKey('literatures.id')),
)

author_literature_rel = Table(
	'author_literature',
	Base.metadata,
	Column('author_id', Integer, ForeignKey('authors.id'), primary_key = True),
	Column('literature_id', Integer, ForeignKey('literatures.id'), primary_key = True),
)


class Address(Base):
	__tablename__ = 'addresses'
	id=Column(Integer, primary_key=True)
	settlement=Column('settlement', String(100))
	country_name=Column('country_name', String(100))
	country_iso=Column('country_iso', String(100))
	department_id = Column(Integer, ForeignKey('departments.id'))
	department=relationship('Department', back_populates='address')


class Institution(Base):
	__tablename__ = 'institutions'
	id=Column(Integer, primary_key=True)
	name=Column('name', String(255))
	departments = relationship('Department')


class Department(Base):
	__tablename__ = 'departments'
	id=Column(Integer, primary_key=True)
	name=Column('name', String(255))
	address=relationship('Address', uselist=False, back_populates='department')
	institution_id = Column(Integer, ForeignKey('institutions.id'))


class Tag(Base):
	__tablename__ = 'tags'
	id=Column(Integer, primary_key=True)
	name=Column('name', String(100))


class Journal(Base):
	__tablename__ = 'journals'
	id=Column(Integer, primary_key=True)
	name=Column('name', String(500))
	issn=Column('issn', String(9))
	eissn=Column('eissn', String(9))
	publications = relationship('Publication')


class Publication(Base):
	__tablename__ = 'publications'
	id=Column(Integer, primary_key=True)
	volume = Column('volume', String(50))
	issue = Column('issue', String(50))
	journal_id = Column(Integer, ForeignKey('journals.id'))


class Author(Base):
	__tablename__ = 'authors'
	id=Column(Integer, primary_key=True)
	first_name = Column('first_name', String(100))
	last_name = Column('last_name', String(100))
	orcid = Column('orcid', String(19)) # orcid format: xxxx-xxxx-xxxx-xxxx
	emails = relationship('Email')
	literature = relationship(
		'Literature',
		secondary = author_literature_rel,
		back_populates='authors'
	)

class Email(Base):
	__tablename__ = 'emails'
	id=Column(Integer, primary_key=True)
	text = Column('text', String(320)) # theoretically maximum possible email length
	author_id = Column(Integer, ForeignKey('authors.id'))



class Citation(Base):
	__tablename__ = 'citations'
	source_id = Column('source_id', Integer, ForeignKey('literatures.id'), primary_key=True)
	referencing_id = Column('referencing_id', Integer, ForeignKey('literatures.id'), primary_key=True)
	page_start = Column('page_start', String(6)) # Strings because of page formats like Roman numbers etc.
	page_end = Column('page_end', String(6))
	source = relationship('Literature', foreign_keys=[source_id])
	referencing_paper = relationship('Literature', foreign_keys=[referencing_id])

class Literature(Base):
	__tablename__ = 'literatures'
	id=Column(Integer, primary_key=True)
	title=Column('title', String())
	subtitle=Column('subtitle', String())
	abstract = Column('abstract', UnicodeText)
	body = Column('body', UnicodeText)
	url = Column('url', String())
	published_date = Column('published_date', Date)
	doi = Column('doi', String()) # doi doesnt have a predefined maxlength: https://www.doi.org/overview/DOI_article_ELIS3.pdf

	sources = relationship(
		'Literature',
		secondary='citations',
		primaryjoin=id==Citation.referencing_id,
		secondaryjoin=id==Citation.source_id
	)
	authors = relationship(
		'Author',
		secondary=author_literature_rel,
		back_populates='literature'
	)
	tags = relationship(
		'Tag',
		secondary=tag_literature_rel
	)


