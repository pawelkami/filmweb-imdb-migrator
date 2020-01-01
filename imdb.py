import requests
import bs4 as bs
import math
import json


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



