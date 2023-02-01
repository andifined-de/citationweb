from fastapi import FastAPI, Depends
import crud
from services.author import get_all_author_citations
from validation.response.author import AuthorResponse
from validation.request.literature import SearchLiteratureRequest
from validation.response.literature import LiteratureResponse
from validation.response.citation import CitationResponse, AuthorCitationResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from database.transaction import Transaction, get_session
import time

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
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.get('/')
async def home():
    return "welcome home"


@app.get('/literature', response_model=list[LiteratureResponse])
async def get_all_literature(tx: Transaction = Depends(Transaction)):
    with tx:
        response = crud.get_all_literature(tx.session)
        print(response)
        response


@app.get('/literature/{id}', response_model=LiteratureResponse)
async def get_literature(id: int, tx: Transaction = Depends(Transaction)):
    with tx:
        print(id)
        return crud.get_literature(tx.session, SearchLiteratureRequest(id=id))


@app.get('/citations', response_model=list[CitationResponse])
async def get_citation_network(tx: Transaction = Depends(Transaction)):
    with tx:
        result = crud.get_all_citations(tx.session)
        return result


@app.get('/authors', response_model=list[AuthorResponse])
async def get_all_authors(tx: Transaction = Depends(Transaction)):
    with tx:
        return crud.get_all_authors(tx.session)


@app.get('/author-citations', response_model=list[AuthorCitationResponse])
async def get_author_citations(tx: Transaction = Depends(Transaction)):
    return get_all_author_citations(tx)
