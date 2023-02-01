import grobid_tei_xml

from domain.connection import Base, engine
from services.literature import get_create_literature
from validation.request.literature import CreateLiteratureRequest
import glob
from pathlib import Path
from validation.request.author import CreateAuthorRequest


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
	) for c in doc.citations if c.title is not None and c.title != '' and len(c.title) < 500]
	return citations


def run_tei_import():
	root_dir = "./static/tei"

	for file in glob.iglob(root_dir + '**/*.tei.xml', recursive=True):
		text = Path(file).read_text()
		doc = grobid_tei_xml.parse_document_xml(text)
		if doc.header.title is None or doc.header.title == '' or len(doc.header.title) > 500:
			continue
		lit = CreateLiteratureRequest(
			title=doc.header.title,
			doi=doc.header.doi,
			published_date=doc.header.date,
			authors=get_authors(doc),
			citations=get_citations(doc)
		)
		result = get_create_literature(lit)


if __name__ == '__main__':
	Base.metadata.reflect(bind=engine)
	Base.metadata.drop_all(bind=engine)
	Base.metadata.create_all(bind=engine)
	run_tei_import()
