from openpyxl import load_workbook

# from backend.data.actor import Actor
# from backend.data.film import Film
# from backend.data.genre import Genre
# from data.__all_models import Film, Actor, Genre, Favorite
from data import db_session


def main():
    db_session.global_init("db/films.db")

    # wb2 = load_workbook('data/cinema.xlsx')
    # ws = wb2.active
    # for row in ws.values:
    #     print(row[7])
    #     film = Film()
    #     film.name = row[1]
    #     film.year = row[3]
    #     film.description = row[6]
    #     for actor in row[7].split(','):
    #         film.actors.append(Actor(name=actor.strip()))
    #     for genre in row[4].split(','):
    #         film.genres.append(Genre(name=genre.strip()))
    #     db_sess = db_session.create_session()
    #     db_sess.add(film)
    #     db_sess.commit()


if __name__ == '__main__':
    main()
