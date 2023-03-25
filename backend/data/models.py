import sqlalchemy
from backend.data.db_session import SqlAlchemyBase
from sqlalchemy import orm


film_to_actor_table = sqlalchemy.Table(
    'film_to_actor',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('films', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('films.id')
                      ),
    sqlalchemy.Column('actors', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('actors.id')
                      )
)

film_to_genre_table = sqlalchemy.Table(
    'film_to_genre',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('films', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('films.id')
                      ),
    sqlalchemy.Column('genres', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('genres.id')
                      )
)


class Film(SqlAlchemyBase):
    __tablename__ = 'films'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    actors = orm.relationship("Actor",
                              secondary="film_to_actor",
                              backref="films")
    genres = orm.relationship("Genre",
                              secondary="film_to_genre",
                              backref="films")


class Actor(SqlAlchemyBase):
    __tablename__ = 'actors'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)



class Genre(SqlAlchemyBase):
    __tablename__ = 'genres'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)


class Favorite(SqlAlchemyBase):
    __tablename__ = 'favorites'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    film_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("films.id"))
    tg_id = sqlalchemy.Column(sqlalchemy.Integer)


