import os, json

from bs4 import BeautifulSoup
from sl4ng import show, pop, getsource, regenerator
import requests


def get(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    boxes = soup.find_all('div', {'class': 'innerbox'})
    for box in boxes:
        yield (
            box.find('span', {'class': 'colornamespan'}).find('a').text,
            box.find('span', {'class': 'colorhexspan'}).find('a').text,
        )

def get_file(path):
    with open(path, 'rb') as fob:
        soup = BeautifulSoup(fob, 'lxml')
        boxes = soup.find_all('div', {'class': 'innerbox'})
        for box in boxes:
            yield (
                box.find('span', {'class': 'colornamespan'}).find('a').text,
                box.find('span', {'class': 'colorhexspan'}).find('a').text,
            )


def hexes_names(uri, path=False):
    rack = (get, get_file)[path](uri)
    return dict(i[::-1] for i in rack)

def names_hexes(uri, path=False):
    rack = (get, get_file)[path](uri)
    return dict(rack)

def hexes(uri, path=False):
    rack = (get, get_file)[path](uri)
    return [i[1] for i in rack]

def names(uri, path=False):
    rack = (get, get_file)[path](uri)
    return [i[0] for i in rack]


funcs = [hexes_names, names_hexes, names, hexes]

def each(uri, path=False, sort_keys=True, **kwargs):
    """
    Scrape each thing into a json file
    """
    
    for func in funcs:
        fname = f"css_colours-{func.__name__}.json"
        with open(fname, 'w+') as fob:
            json.dump(func(uri, path), fob, sort_keys=sort_keys, **kwargs)
            os.startfile(fname)

def every(uri, path=False, sort_keys=True, **kwargs):
    """
    Scrape every thing into a js file
    """
    fname = 'css_colours.js'
    with open(fname, 'w+') as fob:
        for func in funcs:
            d = json.dumps(func(uri, path), sort_keys=sort_keys, **kwargs)
            fob.write(f'const {func.__name__} = {d}\n')
    os.startfile(fname)


if __name__ == '__main__':
    url = 'https://www.w3schools.com/cssref/css_colors.asp'
    path = './CSS Colors.html'
    # each(path, True)
    every(path, True)
