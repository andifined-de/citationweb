from fastapi import FastAPI

from api.v1.authors import author_router
from api.v1.citations import citation_router

api_v1 = FastAPI()
api_v1.include_router(citation_router, prefix='/citations')
api_v1.include_router(author_router, prefix='/authors')
