import grobid_tei_xml

from database.transaction import Transaction
from database.connection import Base, engine
from validation.request.literature import CreateLiteratureRequest
from schemas.literature import LiteratureCreate
from crud import create_update_literature, create_update_author
import glob
from pathlib import Path
from models import Citation
from validation.request.author import CreateAuthorRequest

from datetime import datetime


def create_citations(doc, session):
	sources = []
	for citation in doc.citations:
		if (citation.title == None):
			print(f'No title for citation of document {citation}')
		else:
			source = create_update_literature(session, CreateLiteratureRequest(
				title=citation.title,
				doi=citation.doi,
				published_date=citation.date
			))
			if (source != None):
				sources.append(source)
			# result.sources.append(source)
	# session.commit()
	# print(result)
	return sources


def create_authors(authors, session):
	db_authors = []
	for a in authors:
		author = create_update_author(session, CreateAuthorRequest(
			first_name=a.given_name,
			last_name=a.surname,
			orcid=a.orcid,
			emails=[a.email]
		))
		db_authors.append(author)
	return db_authors


def get_authors(doc):
	authors = [CreateAuthorRequest(
		first_name=a.given_name,
		last_name=a.surname,
		orcid=a.orcid,
		emails=[e for e in [a.email] if e is not None]
	) for a in doc.header.authors]
	return authors


def get_citations(doc):
	citations = [CreateLiteratureRequest(
		title=c.title,
		doi=c.doi,
		published_date=c.date
	) for c in doc.citations if c.title is not None]
	return citations


def run_tei_import():
	root_dir = "./static/tei"

	session = Transaction()

	for file in glob.iglob(root_dir + '**/*.tei.xml', recursive=True):
		text = Path(file).read_text()
		doc = grobid_tei_xml.parse_document_xml(text)
		if doc.header.title is None or doc.header.title == '':
			continue
		print(get_authors(doc))
		lit = CreateLiteratureRequest(
			title=doc.header.title,
			doi=doc.header.doi,
			published_date=doc.header.date,
			authors=get_authors(doc),
			citations=get_citations(doc)
		)
		result = create_update_literature(session, lit)
		# print(doc.citations)
		if result is None:
			print(doc.header.title)
			continue

		"""
		for citation in doc.citations:
			if (citation.title == None):
				print(f'No title for citation of document {citation}')
				continue
			else:
				source = create_update_literature(session, LiteratureCreate(
					title = citation.title,
					doi = citation.doi,
					published_date = citation.date
				))
				if (result != None and source != None):
					result.sources.append(source)
			#session.commit()
		print(result)
		#print(doc.citations)
		"""
	session.commit()


if __name__ == '__main__':
	Base.metadata.reflect(bind=engine)
	Base.metadata.drop_all(bind=engine)
	Base.metadata.create_all(bind=engine)
	run_tei_import()
