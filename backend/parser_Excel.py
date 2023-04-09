from openpyxl import load_workbook

from data.models import Actor
from data.models import Film
from data.models import Genre
from data.models import Clue
from data import db_session


def main():
    db_session.global_init("db/films.db")

    wb2 = load_workbook('data/cinema.xlsx')
    ws = wb2.active
    db_sess = db_session.create_session()
    for row in ws.values:
        film = Film()
        film.name = row[1]
        film.type = row[2]
        film.year = row[3]
        film.description = row[6]
        if row[5]:
            for clue in row[5].split(','):
                clue = clue.strip()
                if clue:
                    obj = db_sess.query(Clue).filter(Clue.clue == clue).first()
                    if not obj:
                        obj = Clue(clue=clue)
                    film.clues.append(obj)
        if row[7]:
            for actor in row[7].split(','):
                actor = actor.strip()
                if actor:
                    obj = db_sess.query(Actor).filter(Actor.name == actor).first()
                    if not obj:
                        obj = Actor(name=actor)
                    film.actors.append(obj)
        if row[4]:
            for genre in row[4].split(','):
                genre = genre.strip()
                if genre:
                    obj = db_sess.query(Genre).filter(Genre.name == genre).first()
                    if not obj:
                        obj = Genre(name=genre)
                    film.genres.append(obj)

        db_sess.add(film)
        db_sess.commit()


if __name__ == '__main__':
    main()
