from fastapi import APIRouter, FastAPI

from api.v1.citations import citation_router

api_v1 = FastAPI()
api_v1.include_router(citation_router, prefix='/citations')
