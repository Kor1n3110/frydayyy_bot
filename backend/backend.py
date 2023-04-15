from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from data.models import Actor
from data.models import Film
from data.models import Genre
from data.models import Clue
from data.models import Favorite
from data import db_session

app = Flask(__name__)
api = Api(app)

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
        # print(args.keys())
        name = args.get('name')
        year = args.get('year')
        offset = args.get('offset', 0)
        films = db_sess.query(Film)
        if year:
            films = films.filter(Film.year == year)
        if name:
            films = films.filter(Film.name.ilike(f'%{name}%'))
        films = films.limit(10).offset(offset)
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
        types_lst = set()
        films = db_sess.query(Film)
        for film in films:
            types_lst.add(film.type)
        return jsonify(list(types_lst))


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
        if not db_sess.query(Film).get(film_id):
            abort(404, message=f"Film id {film_id} not found")

        if not db_sess.query(Favorite).filter(Favorite.film_id == film_id, Favorite.tg_id == tg_id):
            favorite = Favorite(film_id=film_id, tg_id=tg_id)
            db_sess.add(favorite)
            db_sess.commit()
        return jsonify({'success': 'OK'})


api.add_resource(FilmInfo, '/film/<film_id>')
api.add_resource(FilmList, '/film')
api.add_resource(Genres, '/genre')
api.add_resource(Types, '/type')
api.add_resource(Favorites, '/favorite/<tg_id>')

if __name__ == '__main__':
    db_session.global_init("db/films.db")
    app.run(debug=True)
