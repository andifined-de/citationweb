from pydantic import BaseModel
from typing import Optional


class ReadCitationRequest(BaseModel):
	id: int
