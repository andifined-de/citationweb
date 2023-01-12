from pydantic import BaseModel
from typing import Optional

class AddressBase(BaseModel):
	class Config:
		orm_mode = True

class AddressCreate(AddressBase):
	settlement: str
	country_name: str
	country_iso: str


class AddressUpdate(AddressBase):
	id: int
	settlement: Optional[str]
	country_name: Optional[str]
	country_iso: Optional[str]

