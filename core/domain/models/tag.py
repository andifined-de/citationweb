from sqlalchemy import Column, Integer, String

from domain.connection import Base


class TagModel(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column('name', String(100), index=True)
