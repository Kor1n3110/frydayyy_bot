import datetime

import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase
from sqlalchemy import orm

film_to_actor_table = sqlalchemy.Table(
    'film_to_actor',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('films', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('films.id')
                      ),
    sqlalchemy.Column('actors', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('actors.id')
                      ),
    extend_existing=True
)

film_to_genre_table = sqlalchemy.Table(
    'film_to_genre',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('films', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('films.id')
                      ),
    sqlalchemy.Column('genres', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('genres.id')
                      ),
    extend_existing=True
)

film_to_clues_table = sqlalchemy.Table(
    'film_to_clue',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('films', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('films.id')
                      ),
    sqlalchemy.Column('clues', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('clues.id')
                      ),
    extend_existing=True
)


class Film(SqlAlchemyBase):
    __tablename__ = 'films'
    # __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    trailer = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    movie_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    favorites = orm.relationship("Favorite", back_populates='film')
    actors = orm.relationship("Actor",
                              secondary="film_to_actor",
                              backref="films")
    genres = orm.relationship("Genre",
                              secondary="film_to_genre",
                              backref="films")
    clues = orm.relationship("Clue",
                             secondary="film_to_clue",
                             backref="films")


class Actor(SqlAlchemyBase):
    __tablename__ = 'actors'
    # __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)


class Clue(SqlAlchemyBase):
    __tablename__ = 'clues'
    # __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    clue = sqlalchemy.Column(sqlalchemy.String)


class Genre(SqlAlchemyBase):
    __tablename__ = 'genres'
    # __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)


class Favorite(SqlAlchemyBase):
    __tablename__ = 'favorites'
    # __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    film_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("films.id"))
    tg_id = sqlalchemy.Column(sqlalchemy.Integer)
    film = orm.relationship('Film')


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
