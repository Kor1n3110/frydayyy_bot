import sqlalchemy
from backend.data.db_session import SqlAlchemyBase


class Actor(SqlAlchemyBase):
    __tablename__ = 'actors'
    # __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)