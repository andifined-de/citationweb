from fastapi import FastAPI, Depends
import uvicorn

from api.router import api_v1
from services.author import get_all_author_citations
from validation.response.author import AuthorResponse
from validation.request.literature import SearchLiteratureRequest
from validation.response.literature import LiteratureResponse
from validation.response.citation import CitationResponse, AuthorCitationResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

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

app.mount("/api/v1", api_v1)

"""
@app.get('/literature', response_model=list[LiteratureResponse])
async def get_all_literature():
    return get_all_literature()



@app.get('/literature/{id}', response_model=LiteratureResponse)
async def get_literature(id: int):
    with tx:
        print(id)
        return crud.get_literature(tx.session, SearchLiteratureRequest(id=id))


@app.get('/authors', response_model=list[AuthorResponse])
async def get_all_authors():
    with tx:
        return crud.get_all_authors(tx.session)


@app.get('/author-citations', response_model=list[AuthorCitationResponse])
async def get_author_citations():
    return get_all_author_citations(tx)
"""


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
