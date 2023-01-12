from pydantic import BaseModel


class TagBase(BaseModel):
	class Config:
		orm_mode = True

class TagCreate(TagBase):
	name: str

class TagUpdate(TagBase):
	id: int
	name: str

class TagDelete(TagBase):
	id: int
