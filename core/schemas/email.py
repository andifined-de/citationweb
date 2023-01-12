from pydantic import BaseModel, EmailStr


class EmailBase(BaseModel):
	class Config:
		orm_mode = True

class EmailCreate(EmailBase):
	text: EmailStr

class EmailUpdate(EmailBase):
	id: int
	text: EmailStr

class EmailDelete(EmailBase):
	id: int
