import grobid_tei_xml
from schemas.literature import LiteratureCreate
from crud import create_update_literature
from database import SessionLocal, Base, engine
import glob
from pathlib import Path
from models import Citation

from datetime import datetime


def run_tei_import():
	root_dir = "./static/tei"

	session = SessionLocal()

	for file in glob.iglob(root_dir + '**/*.tei.xml', recursive=True):
		text = Path(file).read_text()
		doc = grobid_tei_xml.parse_document_xml(text)
		literature = LiteratureCreate(
			title = doc.header.title,
			doi = doc.header.doi,
			published_date = doc.header.date
		)
		result = create_update_literature(session, literature)
		#print(doc.citations)
		for citation in doc.citations:
			if (citation.title == None):
				print(f'No title for citation of document {citation}')
			else:
				source = create_update_literature(session, LiteratureCreate(
					title = citation.title,
					doi = citation.doi,
					published_date = citation.date
				))
				if (result != None and source != None):
					result.sources.append(source)
			session.commit()
		print(result)
		#print(doc.citations)

if __name__ == '__main__':

	Base.metadata.reflect(bind=engine)
	Base.metadata.drop_all(bind=engine)
	Base.metadata.create_all(bind=engine)
	run_tei_import()


