import sqlalchemy
from backend.data.db_session import SqlAlchemyBase
from sqlalchemy import orm


# film_to_actor_table = sqlalchemy.Table(
#     'film_to_actor',
#     SqlAlchemyBase.metadata,
#     sqlalchemy.Column('films', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('films.id')
#                       ),
#     sqlalchemy.Column('actors', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('actors.id')
#                       ),
#     extend_existing=True
# )
#
# film_to_genre_table = sqlalchemy.Table(
#     'film_to_genre',
#     SqlAlchemyBase.metadata,
#     sqlalchemy.Column('films', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('films.id')
#                       ),
#     sqlalchemy.Column('genres', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('genres.id')
#                       ),
#     extend_existing=True
# )


class Film(SqlAlchemyBase):
    __tablename__ = 'films'
    # __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    favorites = orm.relationship("Favorite", back_populates='film')
    # actors = orm.relationship("Actor",
    #                           secondary="film_to_actor",
    #                           backref="films")
    # genres = orm.relationship("Genre",
    #                           secondary="film_to_genre",
    #                           backref="films")