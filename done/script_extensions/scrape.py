import os, json

from bs4 import BeautifulSoup
import requests



def gather(uri:str) -> str:
    if os.path.exists(uri):
        with open(uri, 'r') as fob:
            return fob.read()
    else:
        r = requests.get(uri)
        return r.text

def parse(gatherling:str) -> dict:
    return json.loads(gatherling)

def save(parseling:dict, fname='extensions.json') -> dict:
    with open(fname, 'w') as fob:
        json.dump(parseling, fob, sort_keys=True)
        os.startfile(fname)
    return {fname: parseling}






if __name__ == '__main__':
    uri = 'https://raw.githubusercontent.com/fristonio/Resources/master/lang-ext.json'
    g = gather(uri)
    print(g)
    
    p = parse(g)
    print(p)
    
    s = save(p)
    print(s)