import requests
import bs4 as bs
import json
import requests_html
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import re
import random
from time import sleep


def strtr(strng, replace):
    buffer = []
    i, n = 0, len(strng)
    while i < n:
        match = False
        for s, r in replace.items():
            if strng[i:len(s)+i] == s:
                buffer.append(r)
                i = i + len(s)
                match = True
                break
        if not match:
            buffer.append(strng[i])
            i = i + 1
    return ''.join(buffer)


class ImdbConnector(object):
    session = None

    def __init__(self):
        pass

    def get_imdb_id_by_title(self, title):
        # from https://stackoverflow.com/a/10064701/108301
        normalizeChars = {
            'Š' : 'S', 'š' : 's', 'Ð' : 'Dj', 'Ž' : 'Z', 'ž' : 'z', 'À' : 'A', 'Á' : 'A', 'Â' : 'A', 'Ã' : 'A', 'Ä' : 'A',
            'Å' : 'A', 'Æ' : 'A', 'Ç' : 'C', 'È' : 'E', 'É' : 'E', 'Ê' : 'E', 'Ë' : 'E', 'Ì' : 'I', 'Í' : 'I', 'Î' : 'I',
            'Ï' : 'I', 'Ñ' : 'N', 'Ń' : 'N', 'Ò' : 'O', 'Ó' : 'O', 'Ô' : 'O', 'Õ' : 'O', 'Ö' : 'O', 'Ø' : 'O', 'Ù' : 'U', 'Ú' : 'U',
            'Û' : 'U', 'Ü' : 'U', 'Ý' : 'Y', 'Þ' : 'B', 'ß' : 'Ss', 'à' : 'a', 'á' : 'a', 'â' : 'a', 'ã' : 'a', 'ä' : 'a',
            'å' : 'a', 'æ' : 'a', 'ç' : 'c', 'è' : 'e', 'é' : 'e', 'ê' : 'e', 'ë' : 'e', 'ì' : 'i', 'í' : 'i', 'î' : 'i',
            'ï' : 'i', 'ð' : 'o', 'ñ' : 'n', 'ń' : 'n', 'ò' : 'o', 'ó' : 'o', 'ô' : 'o', 'õ' : 'o', 'ö' : 'o', 'ø' : 'o', 'ù' : 'u',
            'ú' : 'u', 'û' : 'u', 'ü' : 'u', 'ý' : 'y', 'þ' : 'b', 'ÿ' : 'y', 'ƒ' : 'f', 'ś' : 's', 'Ś' : 'S',
            'ă' : 'a', 'ș' : 's', 'ț' : 't', 'Ă' : 'A', 'Ș' : 'S', 'Ț' : 'T', ' ' : '_', '/' : ":", '-' : ''
        }

        imdb_title = strtr(title, normalizeChars).lower()

        session = requests.Session()

        data = session.get(f'https://v2.sg.media-imdb.com/suggests/{imdb_title[0]}/{imdb_title}.json').text

        # example output:
        # imdb$the_lord_of_the_rings:_the_two_towers({"v":1,"q":"the_lord_of_the_rings:_the_two_towers","d":[{"l":"The Lord of the Rings: The Two Towers","id":"tt0167261","s":"Elijah Wood, Ian McKellen","y":2002,"q":"feature","vt":3,"i":["https://m.media-amazon.com/images/M/MV5BNGE5MzIyNTAtNWFlMC00NDA2LWJiMjItMjc4Yjg1OWM5NzhhXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",1604,2343],"v":[{"l":"The Lord of the Rings Trilogy on Blu-ray","id":"vi2073101337","s":"2:02","i":["https://m.media-amazon.com/images/M/MV5BODk1MzkwNTA4N15BMl5BanBnXkFtZTgwOTU1ODY3MjI@._V1_.jpg",640,480]},{"l":"A Guide to the Films of Peter Jackson","id":"vi1923201561","s":"1:33","i":["https://m.media-amazon.com/images/M/MV5BZjRmMmNmNDEtNTBmYi00NDU4LWIzYmMtNTJjZTFiMGFmZmM0XkEyXkFqcGdeQW1hZGV0aXNj._V1_.jpg",1920,1080]}]},{"l":"The Lord of the Rings: The Two Towers","id":"tt0347436","s":"Action, Adventure, Fantasy","y":2002,"q":"video game","i":["https://m.media-amazon.com/images/M/MV5BODI0Mzk3OTM4N15BMl5BanBnXkFtZTgwMTM4MTk4MDE@._V1_.jpg",352,500]},{"l":"The Lord of the Rings: The Two Towers","id":"tt9674136","s":"Action, Fantasy","y":2002,"q":"video game","i":["https://m.media-amazon.com/images/M/MV5BZmYxYzM4NjMtYTljOS00MWI0LThhMzEtZDMwOWJlYzZkMTk4XkEyXkFqcGdeQXVyOTcyOTc4Mjc@._V1_.jpg",800,790]},{"l":"Lord of the Rings","id":"tt0154789","s":"Adventure, Fantasy","y":1990,"q":"video game","i":["https://m.media-amazon.com/images/M/MV5BZDFiZDUwYmEtOGIwYS00ZjNhLThkNmMtNjBlMDJlZmRlMDI2XkEyXkFqcGdeQXVyNjExODE1MDc@._V1_.jpg",800,1001]},{"l":"LEGO Lord of the Rings: Two Towers in Two Minutes","id":"tt3562762","s":"Vernon Wells, Chris Osborn","y":2012,"q":"video"},{"l":"On the Set: The Lord of the Rings: The Two Towers","id":"tt10924230","s":"Sean Astin, Orlando Bloom","y":2002,"q":"video"}]})
        data_json = json.loads(data[data.find('(') + 1:data.rfind(')')])

        # pod kluczem 'd' w JSON są przechowywane informacje o filmie
        if 'd' not in data_json:
            return None

        return data_json['d'][0]['id']


    def login(self, login, password):
        self.session = requests_html.HTMLSession()
        self.session.headers['User-Agent'] =  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15'
        self.session.headers['Accept-Language'] = "en,en-US;q=0,5"
        self.session.headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8"

        # wchodzenie na stronę, na ktorej sa rozne sposoby logowania (przez imdb, facebook, google itp.) w celu znalezienia odpowiedniego linku
        data = self.session.get('https://www.imdb.com/registration/signin').text

        # Link faktycznej strony logowania - za pomocą konta IMDb
        soup = bs.BeautifulSoup(data, "html.parser")
        login_page_element = soup.find(text='Sign in with IMDb').parent.parent
        login_page_address = login_page_element.attrs['href']

        # Wejście na stronę za pomocą selenium - inne sposoby są wykrywane jako boty i wymagaja wpisania captchy
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        driver.get(login_page_address)
        driver.find_element_by_id('ap_email').send_keys(login)
        driver.find_element_by_id('ap_password').send_keys(password)
        sleep(random.uniform(1, 3))
        driver.find_element_by_id('signInSubmit').click()
        sleep(random.uniform(1, 3))

        # ustawianie cookies zalogowanej sesji uzytkownika w module requests - bedzie on dalej uzywany bo jest lzejszy
        # i nie wymaga uruchamiania w tym celu specjalnie przegladarki internetowej
        for cookie in driver.get_cookies():
            self.session.cookies.set(cookie['name'], cookie['value'])

        result = self.session.get('https://www.imdb.com/')
        pattern = re.compile('\"userName\":(.*?),')
        username = re.search(pattern, result.text).group(1)
        if username is None or username == 'null':
            raise Exception('Bad credentials or request blocked by bot detection on IMDb. If login data is correct - try again later in a few hours.')

        driver.close()


    def rate_film(self, film_id, rating):
        auth_id = self.__get_auth_id(film_id)
        payload = {
            'auth' : auth_id,
            'tconst' : film_id,
            'rating' : int(rating),
            'tracking_tag' : 'title-maindetails',
            'pageId' : film_id,
            'pageType' : 'title',
            'subpageType' : 'main',
        }

        result = self.session.post('https://www.imdb.com/ratings/_ajax/title', data=payload)

        # result_json = json.loads(result.text)
        #
        # if result_json['status'] != 200:
        #     raise Exception("There was a problem with rating movie id: " + film_id)




    def __get_auth_id(self, film_id):
        if self.session is None:
            raise Exception("There is no logged in session")

        data = self.session.get('http://www.imdb.com/title/' + film_id).text

        soup = bs.BeautifulSoup(data, "html.parser")
        tag = soup.find('div', {'data-auth' : True})
        if tag is None:
            return None

        return tag['data-auth']



