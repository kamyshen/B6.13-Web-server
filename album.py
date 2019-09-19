import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и 
    возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def change_database(new_album):
    """
    Вносит полученные через запрос POST данные в базу
    """
    session = connect_db()
    session.add(new_album)
    session.commit()

def check_original(new_album):
    """
    Проверяет, существует ли в базе альбом с параметрами из POST
    """
    session = connect_db()
    original = session.query(Album).filter(Album.year == new_album.year, 
                         Album.artist == new_album.artist,
                         Album.genre == new_album.genre,
                         Album.album == new_album.album).first()
    return original
