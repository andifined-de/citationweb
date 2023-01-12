from fastapi import FastAPI
import crud
from database import SessionLocal
from schemas.literature import LiteratureRead
from schemas.citation import CitationRead
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    'http://localhost:8000',
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def home():
	return "welcome home"

@app.get('/literature', response_model=list[LiteratureRead])
async def getAllLiterature():
	return crud.get_all_literature(SessionLocal())

@app.get('/literature/{id}', response_model=LiteratureRead)
async def getLiterature(id: int):
    print(id)
    return crud.get_literature(SessionLocal(), LiteratureRead(id = id))


@app.get('/citations', response_model=list[CitationRead])
async def get_citation_network():
	return crud.get_all_citations(SessionLocal())
