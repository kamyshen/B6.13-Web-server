from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request
import paste

import album

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Альбомов {} в нашей базе найдено: {} <br>".format(artist, len(album_names))
        result += "<br>".join(album_names)
    return result

@route("/albums", method="POST")
def add_data():
    new_album = album.Album(
        year=request.forms.get("year"),
        artist=request.forms.get("artist"),
        genre=request.forms.get("genre"),
        album=request.forms.get("album")
            )

    if validate_input(new_album) == 1:
        return HTTPError(409, "Год должен быть числом")
    elif validate_input(new_album) == 2:
        return HTTPError(409, "Год должен быть в формате YYYY")
    elif validate_input(new_album) == 3:
        return HTTPError(409, "Должны быть указаны artist и album")
        
    if album.check_original(new_album):
        return HTTPError(409, "Такой альбом уже существует в базе")
    else:
        album.change_database(new_album)
        return "Данные успешно сохранены"

def validate_input(new_album):
    """
    Функция-валидатор с тремя этапами, где проверяется, что 1) год - число,
        2) год в формате YYYY,
        3) предоставлены album и artist (жанр может быть пропущен)
    """
    try:
        new_album.year = int(new_album.year)
    except:
        return 1
    if not len(str(new_album.year))==4:
        return 2
    if new_album.album == None or new_album.artist == None:
        return 3
         
if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True, server='paste')