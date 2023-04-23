import datetime as dt
from werkzeug.security import generate_password_hash
from data import db_session
from data.models import User
name = input('Введите имя:')
email = input('Введите email:')
hashed_password = generate_password_hash(input('Введите пароль:'))
created_date = dt.datetime.now()
db_session.global_init("db/films.db")
db_sess = db_session.create_session()
user = User()
user.name = name
user.email = email
user.hashed_password = hashed_password
user.created_date = created_date
db_sess.add(user)
db_sess.commit()