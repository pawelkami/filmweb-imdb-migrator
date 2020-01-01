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


def get_imdb_id_by_title(title):
    # from https://stackoverflow.com/a/10064701/108301
    normalizeChars = {
        'Š' : 'S', 'š' : 's', 'Ð' : 'Dj', 'Ž' : 'Z', 'ž' : 'z', 'À' : 'A', 'Á' : 'A', 'Â' : 'A', 'Ã' : 'A', 'Ä' : 'A',
        'Å' : 'A', 'Æ' : 'A', 'Ç' : 'C', 'È' : 'E', 'É' : 'E', 'Ê' : 'E', 'Ë' : 'E', 'Ì' : 'I', 'Í' : 'I', 'Î' : 'I',
        'Ï' : 'I', 'Ñ' : 'N', 'Ń' : 'N', 'Ò' : 'O', 'Ó' : 'O', 'Ô' : 'O', 'Õ' : 'O', 'Ö' : 'O', 'Ø' : 'O', 'Ù' : 'U', 'Ú' : 'U',
        'Û' : 'U', 'Ü' : 'U', 'Ý' : 'Y', 'Þ' : 'B', 'ß' : 'Ss', 'à' : 'a', 'á' : 'a', 'â' : 'a', 'ã' : 'a', 'ä' : 'a',
        'å' : 'a', 'æ' : 'a', 'ç' : 'c', 'è' : 'e', 'é' : 'e', 'ê' : 'e', 'ë' : 'e', 'ì' : 'i', 'í' : 'i', 'î' : 'i',
        'ï' : 'i', 'ð' : 'o', 'ñ' : 'n', 'ń' : 'n', 'ò' : 'o', 'ó' : 'o', 'ô' : 'o', 'õ' : 'o', 'ö' : 'o', 'ø' : 'o', 'ù' : 'u',
        'ú' : 'u', 'û' : 'u', 'ü' : 'u', 'ý' : 'y', 'þ' : 'b', 'ÿ' : 'y', 'ƒ' : 'f',
        'ă' : 'a', 'ș' : 's', 'ț' : 't', 'Ă' : 'A', 'Ș' : 'S', 'Ț' : 'T', ' ' : '_'
    }

    imdb_title = strtr(title, normalizeChars).lower()

    session = requests.Session()

    data = session.get(f'https://v2.sg.media-imdb.com/suggests/{imdb_title[0]}/{imdb_title}.json').text
    data_json = json.loads(data[data.find('(') + 1:data.rfind(')')])

    # pod kluczem 'd' w JSON są przechowywane informacje o filmie
    if 'd' not in data_json:
        return None

    # w kluczu 'l' jest przechowywany tytuł w IMDB
    if data_json['d'][0]['l'] != title:
        return None

    return data_json['d'][0]['id']

