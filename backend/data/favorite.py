import sqlalchemy
from backend.data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class Favorite(SqlAlchemyBase):
    __tablename__ = 'favorites'
    # __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    film_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("films.id"))
    tg_id = sqlalchemy.Column(sqlalchemy.Integer)
    film = orm.relationship('Film')