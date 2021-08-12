"""
find stream on main page
find
"""
import requests, os
from bs4 import BeautifulSoup
from sl4ng import pop, show

HEADERS = {
    'user-agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
        'AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/45.0.2454.101 Safari/537.36'
    ),
    # 'referer': 'http://stats.nba.com/scores/'
}

def scrape(url):
    name = 'vimeo_object.json'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    
    res = [*filter(lambda x: x['type']=="application/ld+json", soup.find_all('script', type=True))][0]
    json = eval(next(res.descendants).strip()[1:-1].replace('true', 'True'))#[1]
    jso = json.loads(next(res.descendants).strip())
    return json

def pretty(url):
    with requests.get(url) as r:
        soup = BeautifulSoup(r.text, 'lxml').prettify()
        print(soup)
        return soup





if __name__ == '__main__':
    bed = "https://player.vimeo.com/video/237282867"
    
    txt = BeautifulSoup(bytes(pretty(bed), 'utf-8'), 'lxml')
    
    url = "https://vimeo.com/237282867"
    
    # res = scrape(url)
    # print(res)
    # show(res[0].values())
    # show(res[1].values())
    # show(res)
    # o
    