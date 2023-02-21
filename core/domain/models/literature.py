from sqlalchemy import Integer, Column, Table, ForeignKey, String, Date, select, text, table, column, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
import sqlalchemy_utils

from domain.connection import Base, engine
from domain.models.citation import CitationModel
from domain.models.tag import TagModel

tag_literature_rel = Table(
    'tag_literature',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id'), index=True),
    Column('literature_id', Integer, ForeignKey('literatures.id'), index=True),
)

author_literature_rel = Table(
    'author_literature',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id'), index=True),
    Column('literature_id', Integer, ForeignKey('literatures.id'), index=True),
)


class LiteratureModel(Base):
    __tablename__ = 'literatures'
    id = Column(Integer, primary_key=True, index=True)
    title = Column('title', String(), index=True)
    subtitle = Column('subtitle', String())
    # abstract = Column('abstract', UnicodeText)
    # body = Column('body', UnicodeText)
    url = Column('url', String())
    published_date = Column('published_date', Date)
    doi = Column('doi', String(), index=True)

    # doi doesnt have a predefined maxlength: https://www.doi.org/overview/DOI_article_ELIS3.pdf

    @hybrid_property
    def citation_score(self):
        return len(self.cited_by) + 1  # add one to have a non zero node size

    citations = relationship(
        'LiteratureModel',
        secondary='citations',
        primaryjoin=id == CitationModel.cited_id,
        secondaryjoin=id == CitationModel.citing_id,
        backref='cited_by',
        lazy='joined',
        join_depth=1
    )
    authors = relationship(
        'AuthorModel',
        secondary=author_literature_rel,
        back_populates='literature',
        join_depth=1
    )
    tags = relationship(
        TagModel,
        secondary=tag_literature_rel,
        backref='literature',
        join_depth=1
    )


c = table('citations', column('cited_id'), column('citing_id'))
l1 = table('literatures', column('id'), column('title')).alias('l1')
l2 = table('literatures', column('id'), column('title')).alias('l2')
count_query = select([
    column('cited_id'),
    func.count('cited_id').label('citation_score')
]).select_from(c).group_by('cited_id').subquery()
citation_query = select([
    column('cited_id'),
    column('citing_id'),
    text('l1.title as cited_title'),
    text('l2.title as citing_title')
]).select_from(c).join(l1, c.c.cited_id == l1.c.id).join(l2, c.c.citing_id == l2.c.id).subquery().alias('cit')
citation_literature_view = select([
    text('cit.cited_id as cited_id'),
    column('citing_id'),
    column('cited_title'),
    column('citing_title'),
    column('citation_score')
]).select_from(citation_query).join(count_query, count_query.c.cited_id == citation_query.c.cited_id)
print(str(citation_literature_view))
sqlalchemy_utils.create_materialized_view('citation_literature_view', citation_literature_view, Base.metadata)


"""
select
	sub.cited_id,
	citing_id,
	cited_title,
	citing_title,
	citation_score
from (SELECT
		citations.cited_id as cited_id,
		citing_id,
		l1.title as cited_title,
		l2.title as citing_title
	FROM citations
	JOIN literatures AS l1 ON citations.cited_id = l1.id
	JOIN literatures AS l2 ON citations.citing_id = l2.id
) AS sub join (
	select cited_id, count(cited_id) as citation_score from citations group by cited_id
) as count_sub on sub.cited_id = count_sub.cited_id order by citation_score desc
"""