import filmweb
import imdb

if __name__ == '__main__':
    filmweb_login = input("Filmweb email/login: ")
    filmweb_password = input("Filmweb password: ")

    filmweb_connector = filmweb.FilmwebConnector(filmweb_login, filmweb_password)
    print('Logged in filmweb successfully')

    all_ratings = filmweb_connector.get_all_filmweb_rates()
    all_ratings.reverse()

    imdb_login = input("IMDb email: ")
    imdb_password = input("IMDb password: ")
    imdb_connector = imdb.ImdbConnector()
    imdb_connector.login(imdb_login, imdb_password)

    not_found_on_imdb = []

    for rating in all_ratings:
        imdb_id = imdb_connector.get_imdb_id_by_title(rating.title)
        if imdb_id is None:
            print(f"ID for {rating.title} was not found")
            not_found_on_imdb.append(rating)
            continue

        imdb_connector.rate_film(imdb_id, rating.rating)
        print(f'Successfully added rating for {rating.title}')
