import filmweb
import imdb

if __name__ == '__main__':
    filmweb_login = input("Filmweb email/login: ")
    filmweb_password = input("Filmweb password: ")

    filmweb_connector = filmweb.FilmwebConnector(filmweb_login, filmweb_password)

    all_ratings = filmweb_connector.get_all_filmweb_rates()

    imdb_connector = imdb.ImdbConnector()

    not_found_on_imdb = []

    for rating in all_ratings:
        imdb_id = imdb_connector.get_imdb_id_by_title(rating.title)
        if imdb_id is None:
            print(f"ID for {rating.title} was not found")
            not_found_on_imdb += rating
            continue
