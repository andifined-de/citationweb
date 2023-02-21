from sqlalchemy import Column, Integer, ForeignKey, String, select
from sqlalchemy.orm import relationship
from domain.connection import Base


class CitationModel(Base):
    __tablename__ = 'citations'
    id = Column(Integer, primary_key=True, index=True)  # todo: fix insert error
    cited_id = Column('cited_id', Integer, ForeignKey('literatures.id'), index=True)
    citing_id = Column('citing_id', Integer, ForeignKey('literatures.id'), index=True)
    cited = relationship('LiteratureModel', foreign_keys=[cited_id], viewonly=True, lazy='joined', join_depth=1)
    citing = relationship('LiteratureModel', foreign_keys=[citing_id], viewonly=True, lazy='joined', join_depth=1)


class FlatCitationModel(Base):
    __tablename__ = 'citation_literature_view'
    cited_id = Column('cited_id', Integer, ForeignKey('literatures.id'), primary_key=True)
    citing_id = Column('citing_id', Integer, ForeignKey('literatures.id'), primary_key=True)
    cited_title = Column('cited_title', String)
    citing_title = Column('citing_title', String)
    citation_score = Column('citation_score', Integer)
