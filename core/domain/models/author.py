from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from domain.connection import Base
from domain.models.literature import author_literature_rel


class EmailModel(Base):
    __tablename__ = 'emails'
    id = Column(Integer, primary_key=True)
    text = Column('text', String(320))  # theoretically maximum possible email length
    author_id = Column(Integer, ForeignKey('authors.id'))


class AuthorModel(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column('first_name', String(100), index=True)
    middle_name = Column('middle_name', String(100), index=True)
    last_name = Column('last_name', String(100), index=True)
    orcid = Column('orcid', String(19), index=True)  # orcid format: xxxx-xxxx-xxxx-xxxx
    emails = relationship('EmailModel')

    @hybrid_property
    def full_name(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'

    @hybrid_property
    def citation_score(self):
        score = 1
        for lit in self.literature:
            score += lit.citation_score
        return score

    literature = relationship(
        'LiteratureModel',
        secondary=author_literature_rel,
        back_populates='authors',
        lazy='subquery',
        join_depth=1
    )
