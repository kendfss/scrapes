"""\
Scrape (and listen to) the html and/or text of an adblocked (and any other non-bot-weary) webpage\
"""
# ```
import os, re, urllib, json
from itertools import tee

import requests, pyttsx3
from bs4 import BeautifulSoup
from bs4.element import Script
from tqdm import tqdm

from sl4ng import show, join, pop, regenerator, clean_url


HEADERS = {
    'user-agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
        'AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/45.0.2454.101 Safari/537.36'
    ),
    # 'referer': 'http://stats.nba.com/scores/'
}


def scrape_album(url) -> list:
    """
    Scrape tracks, artwork, and some other metadata, from an album on a bandcamp profile page; as well as the artist/label's display picture.
    Not yet tested on a track.
    Will break if any of the listed content is not playable
    """
    url = clean_url(url)
    # r = requests.get(url, headers=HEADERS)
    r = requests.get(url)#, headers=HEADERS)
    soup = BeautifulSoup(r.text,'lxml')
    
    refs = [*filter(lambda x: x['type']=="application/ld+json", soup.find_all('script', type=True))]
    # print(refs)
    # return refs[0]
    refs = json.loads(next(refs[0].descendants).strip())
    # refs = eval(str(refs[0]).splitlines()[1].strip().replace('true', 'True'))
    # refs 
    
    track_data = refs['track']['itemListElement']
    album = dict()
    for track in track_data:
        try:
            d = { 
                'name': track['item']['name'],
                'number': track['item']['additionalProperty'][4]['value'],
                'stream': track['item']['additionalProperty'][2]['value'],
                'format': track['item']['additionalProperty'][2]['name']
            }
            album[d['number']] = d
        except IndexError:
            continue
    lines = map(str.strip, """album['art'] = refs['image']
    album['desc'] = refs['description']
    album['date'] = refs['datePublished']
    album['artist'] = {'name': refs['byArtist']['name'], 'photo': refs['byArtist']['image']}
    album['title'] = refs['name']
    album['url'] = refs['@id']
    album['tags'] = [*map(str.strip, refs['keywords'].split(','))]""".splitlines())
    for line in lines:
        try:
            exec(line)
        except KeyError:
            continue
    return album

def scrape_track(url) -> list:
    """
    Scrape tracks, artwork, and some other metadata, from an album on a bandcamp profile page; as well as the artist/label's display picture.
    Not yet tested on a track.
    Will break if any of the listed content is not playable
    """
    url = clean_url(url)
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text,'lxml')
    
    refs = [*filter(lambda x: x['type']=="application/ld+json", soup.find_all('script', type=True))]
    data = eval(str(refs[0]).splitlines()[1].strip().replace('true', 'True'))
    # print(data)
    # return data
    # data = refs
    track = {}
    lines = map(str.strip, """'url'* data['additionalProperty'][2]['value']
    'title'* data['name']
    'artist'* {'name': data['byArtist']['name'], 'photo': data['byArtist']['image'],}
    'artwork'* data['image']
    'description'* data['description']
    'lyrics'* data['recordingOf']['lyrics']['text']""".splitlines())
    for line in lines:
        key, val = line.split('*')
        
        try:
            val = eval(val.strip())
            print(key, val)
            exec(f'track[{key}] = "{val}"')
        except KeyError:
            continue
    return track


def download_file(url, track_name, chunk_size=1024):
    r = requests.get(url, stream=True)
    print(r.headers)
    total_size = int(l if (l:=r.headers.get('content-length')) else 0)
    size = f"{total_size:,} kb"
    
    track_name = url.split('/')[-1].split('?')[0].replace('-', ' ')
    artist = url.split('/')[2].split('.')[0]
    album = url.split('/')[4].replace('-', ' ').title()
    folder = os.path.join('bandcamp_downloads', artist, album)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, track_name)
    
    print(track_name, size, sep="\n")
    with open(path, 'wb') as f:
        for data in tqdm(
                            iterable=r.iter_content(chunk_size=chunk_size), 
                            total=total_size/chunk_size if total_size else None, 
                            unit='KB'
                        ):
            f.write(data)
    pop(folder)

class Ripper:
    def __new__(cls, url):
        pass
    


 

if __name__ == '__main__':
    
    url = 'https://shadesxshades.bandcamp.com/album/sample-pack-one'
    url = 'https://microfunk.bandcamp.com/album/synths-sample-pack'
    url = 'https://leonvynehall.bandcamp.com/album/rojus-designed-to-dance'
    url = 'https://kaiwhiston.bandcamp.com/album/no-world-as-good-as-mine'
    url = 'https://afrolab9000.bandcamp.com/album/so-the-flies-dont-come'
    url = 'https://errorbroadcast.bandcamp.com/album/2nd'
    # links = scrape_album(url)
    url = 'https://boyoomconnective.bandcamp.com/track/dinosaur'
    
    # links = scrape_track(url)
    links = []
    urls = "https://shogunaudioalixperez.bandcamp.com/album/resolution-vanguard https://tirzah.bandcamp.com/album/devotion https://billywoods.bandcamp.com/album/hiding-places https://billywoods.bandcamp.com/album/terror-management https://exitrecords.co.uk/album/exit071-skeptical-alix-perez-without-a-trace-ep https://raffybushman.bandcamp.com/album/look-up https://soulofzurich.bandcamp.com/album/kamalas-danz"
    for album in urls:
        links.append(scrape_album(album))
    show(links, enum=True)
