import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template, redirect
from flask_login import login_required, logout_user, login_user, LoginManager, current_user
from flask_restful import reqparse, abort, Api, Resource
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, PasswordField, EmailField, StringField, TextAreaField
from wtforms.validators import DataRequired

from data.models import Actor, User
from data.models import Film
from data.models import Genre
from data.models import Clue
from data.models import Favorite
from data import db_session

app = Flask(__name__)
api = Api(app)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")

parser = reqparse.RequestParser()
parser.add_argument('task')


class FilmInfo(Resource):
    def get(self, film_id):
        db_sess = db_session.create_session()
        film = db_sess.query(Film).filter(Film.id == film_id).first()
        actors = film.actors
        genres = film.genres
        film_info = {
            "name": film.name,
            "year": film.year,
            "description": film.description,
            "type": film.type,
            "trailer": film.trailer,
            "movie_link": film.movie_link,
            "actors": [actor.name for actor in actors],
            "genres": [genre.name for genre in genres],
        }
        return jsonify(film_info)


class FilmList(Resource):
    def get(self):
        db_sess = db_session.create_session()
        args = request.args
        genres = args.getlist('genres')
        actors = args.getlist('actors')
        details = args.getlist('details')
        offset = args.get('offset', 1)
        films = db_sess.query(Film)
        if genres:
            genres_ids = [
                db_sess.query(Genre.id).filter(Genre.name.ilike(f'%{search}%')).distinct().all()
                for search in genres]
            ids = []
            for _ids in genres_ids:
                ids += _ids
            genres_ids = [genre[0] for genre in ids]
            films = films.join(Film.genres).filter(Genre.id.in_(genres_ids))
        if actors:
            # actor_ids = [db_sess.query(Actor.id).filter(Actor.name.ilike(f'%{search}%')).scalar() for
            #              search in actors]
            actor_ids = [
                db_sess.query(Actor.id).filter(Actor.name.ilike(f'%{search}%')).distinct().all()
                for search in actors]
            ids = []
            for _ids in actor_ids:
                ids += _ids
            actor_ids = [actor[0] for actor in ids]
            films = films.join(Film.actors).filter(Actor.id.in_(actor_ids))
        if details:
            # details_ids = [db_sess.query(Clue.id).filter(Clue.clue.ilike(f'%{search}%')).scalar() for
            #                search in details]
            detail_ids = [
                db_sess.query(Clue.id).filter(Clue.clue.ilike(f'%{search}%')).distinct().all()
                for search in details]
            ids = []
            for _ids in detail_ids:
                ids += _ids
            detail_ids = [detail[0] for detail in ids]
            films = films.join(Film.clues).filter(Clue.id.in_(detail_ids))
        films = films.limit(6).offset(offset).all()
        films_response = [{'id': film.id, 'name': film.name} for film in films]
        return jsonify(films_response)


class Genres(Resource):
    def get(self):
        db_sess = db_session.create_session()
        genres_lst = []
        genres = db_sess.query(Genre)
        for genre in genres:
            genres_lst.append({'id': genre.id, 'name': genre.name})
        return jsonify(genres_lst)


class Types(Resource):
    def get(self):
        db_sess = db_session.create_session()
        types = [typ[0] for typ in db_sess.query(Film.type).distinct()]
        return jsonify(types)


class Favorites(Resource):
    def get(self, tg_id):
        db_sess = db_session.create_session()
        favorites = db_sess.query(Favorite).filter(Favorite.tg_id == tg_id)
        favorite_lst = []
        for favorite in favorites:
            name = favorite.film.name
            favorite_lst.append({'id': favorite.film_id, 'name': name})
        return jsonify(favorite_lst)

    def post(self, tg_id):
        db_sess = db_session.create_session()
        args = request.json
        film_id = args.get('film_id')
        if not db_sess.get(Film, film_id):
            abort(404, message=f"Film id {film_id} not found")
        if not db_sess.query(Favorite).filter(Favorite.film_id == film_id,
                                              Favorite.tg_id == tg_id).first():
            print('ok')
            favorite = Favorite(film_id=film_id, tg_id=tg_id)
            db_sess.add(favorite)
            db_sess.commit()
        return jsonify({'success': 'OK'})

    def delete(self, tg_id):
        db_sess = db_session.create_session()
        film_id = request.args.get('film_id')
        if not db_sess.query(Favorite).filter(Favorite.film_id == film_id,
                                              Favorite.tg_id == tg_id).first():
            abort(404, message=f"Entry not found")
        db_sess.query(Favorite).filter(Favorite.film_id == film_id, Favorite.tg_id == tg_id).delete()
        db_sess.commit()
        return jsonify({'deleted': f'{film_id}'})


@app.route('/edit_film/<int:film_id>', methods=['GET', 'POST'])
@login_required
def edit_news(film_id):
    form = FilmsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        film = db_sess.query(Film).filter(Film.id == film_id).first()
        if film:
            form.name.data = film.name
            form.description.data = film.description
            form.year.data = film.year
            form.trailer.data = film.trailer
            form.movie_link.data = film.movie_link
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        film = db_sess.query(Film).filter(Film.id == film_id).first()
        if film:
            film.name = form.name.data
            film.description = form.description.data
            film.year = form.year.data
            film.trailer = form.trailer.data
            film.movie_link = form.movie_link.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('edit.html',
                           title='Редактирование',
                           form=form
                           )


# class SuperUser(Resource):
#     def get(self, film_id):
#         form = FilmsForm()
#         db_sess = db_session.create_session()
#         film = db_sess.query(Film).filter(Film.id == film_id).first()
#         if film:
#             form.name.data = film.name
#             form.description.data = film.description
#             form.year.data = film.year
#             form.trailer.data = film.trailer
#             form.movie_link.data = film.movie_link
#             return render_template('edit.html',
#                                    title='Редактирование',
#                                    form=form
#                                    )
#         else:
#             abort(404)
#
#     def post(self):
#         form = FilmsForm()
#         if form.validate_on_submit():
#             db_sess = db_session.create_session()
#             film = db_sess.query(Film).filter(Film.id == film_id).first()
#             if film:
#                 film.name = form.name.data
#                 film.description = form.description.data
#                 film.year = form.year.data
#                 film.trailer = form.trailer.data
#                 film.movie_link = form.movie_link.data
#                 db_sess.commit()
#                 return redirect('/')
#             else:
#                 abort(404)
#         return render_template('edit.html',
#                                title='Редактирование',
#                                form=form
#                                )


class FilmsForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    year = StringField("Год")
    description = TextAreaField("Описание")
    type = StringField("Тип")
    trailer = StringField("Трейлер")
    movie_link = StringField("Смотреть фильм")
    submit = SubmitField('Применить')


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
@login_required
def news():
    db_sess = db_session.create_session()
    films = db_sess.query(Film).all()
    return render_template('film_tabl.html', films=films)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


api.add_resource(FilmInfo, '/film/<film_id>')
api.add_resource(FilmList, '/film')
api.add_resource(Genres, '/genre')
api.add_resource(Types, '/type')
api.add_resource(Favorites, '/favorite/<tg_id>')

if __name__ == '__main__':
    db_session.global_init("db/films.db")
    app.run(debug=True)
