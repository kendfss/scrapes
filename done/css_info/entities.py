import os, json

from bs4 import BeautifulSoup
from sl4ng import show, pop, getsource, regenerator, multisplit
import requests


def get_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    rows = soup.find('table', {'class': 'w3-table-all notranslate charset-tryit'}).find_all('tr')[1:]
    for row in rows:
        yield map(
            lambda x: x.text,
            row.find_all('td')
        )
def get_path(path):
    with open(path, 'rb') as fob:
        soup = BeautifulSoup(fob, 'lxml')
        rows = soup.find('table', {'class': 'w3-table-all notranslate charset-tryit'}).find_all('tr')[1:]
        for row in rows:
            yield map(
                lambda x: x.text,
                row.find_all('td')
            )

def by_id(uri, getter=get_url):
    d = {}
    for char, entity, name in getter(uri):
        d[entity] = {
            'char': char,
            'name': name,
        }
    return d

def by_name(uri, getter=get_url):
    d = {}
    for char, entity, name in getter(uri):
        d[name] = {
            'char': char,
            'id': entity,
        }
    return d

def by_char(uri, getter=get_url):
    d = {}
    for char, entity, name in getter(uri):
        d[char] = {
            'name': name,
            'id': entity,
        }
    return d




if __name__ == '__main__':
    url = 'https://www.w3schools.com/cssref/css_entities.asp'
    path = './CSS Entities.html'
    names = 'by_id.json by_name.json by_char.json'.split()
    
    for name in names:  
        fname = f"css_entities-{name}"
        with open(fname, 'w') as fob:
            func = eval(f'{list(multisplit("-.", name))[-2]}')
            json.dump(func(url), fob, sort_keys=True)
            # json.dump(func(path, get_path), fob, sort_keys=True)
            os.startfile(fname)