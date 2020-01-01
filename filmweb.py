import requests
import bs4 as bs
import math
import json

# maksymalna liczba filmów wyświetlanych na stronie
MAX_COUNT_FOR_PAGE = 25.0


class FilmRate(object):
    title_pl = ""
    title = ""
    rating = 1.0
    year = 1900

    def __str__(self):
        return '{"titlePl" : "%s", "title" : "%s", "rating": %s, "year" : %s}' % (self.title_pl, self.title, self.rating, self.year)

    def __repr__(self):
        return str(self)


class FilmwebConnector(object):
    session = None
    username = None


    def __init__(self, login, password):
        self.login_to_filmweb(login, password)


    def __create_rates_dict(self, soup):
        rates_dict = {}
        user_votes_div = soup.find('div', attrs={'class' : 'userVotesPage__results'})

        for el in user_votes_div.find_all('script', attrs={'type' : 'application/json'}):
            j = json.loads(el.contents[0])
            rates_dict[j['eId']] = j['r']

        return rates_dict


    def __get_rate_from_div(self, soup_div, rates_dict):
        rate = FilmRate()
        rate.year = int(soup_div.find('div', attrs={'class', 'filmPreview__extraYear'}).contents[0].strip())
        film_rate_div = soup_div.find('div', attrs={'class' : 'UserRateFilm'})
        rate.rating = float(rates_dict[int(film_rate_div.attrs['data-id'])])

        rate.title_pl = soup_div.find('h3', attrs={'class', 'filmPreview__title'}).contents[0].strip()
        orig_title = soup_div.find('div', attrs={'class', 'filmPreview__originalTitle'})
        if not orig_title:
            rate.title = rate.title_pl
        else:
            rate.title = orig_title.contents[0].strip()

        return rate


    def get_rates_on_page(self, path, page_num):
        data = self.session.get(f'https://www.filmweb.pl/user/{self.username}/{path}?page={page_num}').text

        film_rates = []

        soup = bs.BeautifulSoup(data, "html.parser")
        rates_dict = self.__create_rates_dict(soup) # oceny są przetrzymywane w innym miejscu i wczytywane przez JavaScript - dlatego tworzę z nich słownik
        for rate in soup.find_all('div', attrs={'class' : 'voteBoxes__box'}):
            film_rates.append(self.__get_rate_from_div(rate, rates_dict)) # todo

        return film_rates


    def get_rates(self, path):
        data = self.session.get(f'https://www.filmweb.pl/user/{self.username}/{path}').text
        soup = bs.BeautifulSoup(data, "html.parser")

        supa = soup.find('span', attrs={'class': 'blockHeader__titleInfoCount'})

        title_count = int(supa.contents[0].strip())
        print(path + str(title_count))

        page_count = math.ceil(title_count / MAX_COUNT_FOR_PAGE)

        rates = []
        for i in range(1, page_count + 1):
            rates += self.get_rates_on_page(path, i)

        return rates


    def get_film_rates(self):
        return self.get_rates('films')


    def get_serials_rates(self):
        return self.get_rates('serials')


    def get_games_rates(self):
        return self.get_rates('games')


    def get_all_filmweb_rates(self):
        return self.get_film_rates() + self.get_serials_rates() + self.get_games_rates()


    def login_to_filmweb(self, login, password):
        self.session = requests.Session()
        payload = {'j_username' : login, 'j_password' : password}

        result = self.session.post('https://www.filmweb.pl/j_login', data=payload)
        if 'bad.credentials' in result.url:
            raise Exception('Invalid credentials')

        self.username = self.get_logged_username()


    def get_logged_username(self):
        data = self.session.get('https://www.filmweb.pl/my').text

        soup = bs.BeautifulSoup(data, "html.parser")
        supa = soup.find('span', attrs={'class' : 'user__name-wrap'})
        username = supa.contents[0].strip()

        return username



filmweb_login = input("Filmweb email/login: ")
filmweb_password = input("Filmweb password: ")

filmweb = FilmwebConnector(filmweb_login, filmweb_password)

all_titles = filmweb.get_all_filmweb_rates()
