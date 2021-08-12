"""

"""

import os, json

from bs4 import BeautifulSoup
from sl4ng import show, pop, getsource, regenerator, multisplit, flat
import requests, pyperclip as pc

def get_path(path):
    with open(path, 'rb') as fob:
        soup = BeautifulSoup(fob, 'lxml')
        rows = soup.find('table', {'class': "CALSTABLE"}).find_all('tr')[1:]
        d = {}
        for code, description, example, meaning in rows:
            c = ''.join(multisplit('+*', code.text)[0])
            d[int(c)] = {
                'description': description.text,
                'example': example.text,
                'meaning': meaning.text,
            }
        return d




if __name__ == '__main__':
    path = r'.\Exit Codes With Special Meanings.html'
    name = 'exit_codes.json'
    with open(name, 'w') as fob:
        json.dump(get_path(path), fob, sort_keys=True)
        os.startfile(name)
    
    
    