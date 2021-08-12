import os, json, re

from bs4 import BeautifulSoup
import requests

from sl4ng import show, pop, getsource


def cast_number(string):
    try:
        return (float, int)[isint(string)](string)
    except ValueError:
        return int(float(string))

def isint(string):
    string = str(string)
    numeric = all(map(str.isnumeric, splitter('-.')(string)))
    periods = string.count('.')
    negs = string.count('-')
    if periods > 1 or negs > 1 or not numeric:
        raise ValueError
    elif periods == 0:
        return True
    elif not any(map(int, string.split('.')[-1])):
        return True
    return False

def isint(string):
    string = str(string)
    numeric = all(map(str.isnumeric, splitter('-.')(string)))
    periods = string.count('.')
    negs = string.count('-')
    if periods > 1 or negs > 1 or not numeric:
        raise ValueError
    elif periods == 0:
        return True
    elif not any(map(int, string.split('.')[-1])):
        return True
    return False

def fix_magnitude(string):
    string = ''.join(splitter([' ', '...'])(str(string)))
    if (match := re.search('e\d+$|e(\-)*\d+$', string)):
        parts = map(str.strip, (string[:match.start()], string[match.start()+1:]))
        operand, power = parts
        operand = cast_number(operand)
        factor = 10 ** cast_number(power)
        return operand * factor
    elif (match := re.search('exact', string)):
        string = 0
    return cast_number(string)

def fix_unit_power(sub):
    if (match := re.search('\w+\^\-\d+|\((.)+\)\^\-\d+', sub)):
        *dim, power = sub.split('^')
        dim = '^'.join(dim)
        power = '' if power=='-1' else power[1:]
        sub = f"/{dim}^{power}" if power else f"/{dim}"
    return sub

def fix_unit_operations(result):
    for i, part in enumerate(result[1:], 1):
        op = ('·', '')[part.startswith('/')]
        result[i] = op + part
    if result:
        head = '1' if result[0].startswith('/') else ''
        result = head + ''.join(result)
    return ''.join(result)

def gather_unit_operations(string):
    if len(parts := string.split('/')) == 3:
        first, second, third = parts
        pred = second.startswith('(') or third.endswith(')')
        string = f"{first}/{second}·{third}" if pred else f"{first}/({second}·{third})"
    return string

def fix_units(string):
    units = string.split()
    result = [*map(fix_unit_power, string.split())]
    result = fix_unit_operations(result)
    return gather_unit_operations(result)

def units(path, index):
    return {const['units'] for const in parse(path, index).values()}

def values(path, index):
    return {const['value'] for const in parse(path, index).values()}

def uncertainties(path, index):
    return {const['uncertainty'] for const in parse(path, index).values()}

def check(path, index):
    assert all(isinstance(i, str) for i in units(path, index))
    assert all(isinstance(i, (int, float)) for i in values(path, index))
    assert all(isinstance(i, (int, float)) for i in uncertainties(path, index))
    return scrape(path, index)



def gather(uri:str) -> str:
    if os.path.exists(uri):
        with open(uri, 'rb') as fob:
            soup = BeautifulSoup(fob, 'lxml')
    else:
        r = requests.get(uri)
        soup = BeautifulSoup(r.text, 'lxml')
    return soup.find(
        'table', 
        {"class": "wikitable sortable collapsible mw-collapsible mw-made-collapsible jquery-tablesorter"}
    ).find_all('tr')[1:]

def parse_note_refs(datum):
    if (m := re.search('(\[[IVX]+\])+$', datum)):
        notes, datum = datum[m.start():], datum[:m.start()]
    else:
        notes, datum = '', datum
    return notes, remove_braces(datum)

def remove_braces(datum):
    number = "\d+(\.\d*)?"
    braces = "(\[|\(){}(\)|\])"
    if (m := re.match(braces.format(number), datum)):
        substr = datum[m.start(): m.end()]
        open, *datum, close = substr
        datum = ''.join(datum)
    return datum

def parse(gatherling:str) -> dict:
    titles = gatherling[0]
    units = gatherling[1]
    elements = gatherling[3:-1]
    notes = gatherling[-1]
    table = {
        "elements": {},
        "info": {},
    }
    for row in elements:
        row = map(str.strip, [i.text for i in row.find_all('td')])
        number, symbol, element, etymology, group, period, weight, density, melting, boiling, shc, negativity, abundance = row
        parts = [number, symbol, element, etymology, group, period, weight, density, melting, boiling, shc, negativity, abundance]
        parts = [*map(parse_note_refs, parts)]
        deets = [i[0] for i in parts]
        data = [i[1] for i in parts]
        number, symbol, element, etymology, group, period, weight, density, melting, boiling, shc, negativity, abundance = data
        # print([number, symbol, element, etymology, group, period, weight, density, melting, boiling, shc, negativity, abundance])
        print([number, symbol, element, group, period, weight, density, melting, boiling, shc, negativity, abundance])
        print(deets)
        table['elements'][element] = {
            "number": number, 
            "symbol": symbol, 
            "etymology": etymology, 
            "group": group, 
            "period": period, 
            "weight": weight, 
            "density": density, 
            "melting": melting, 
            "boiling": boiling, 
            "shc": shc, 
            "negativity": negativity, 
            "abundance": abundance, 
            "details": deets
        }
    table['info']['titles'] = [i.text for i in titles.find_all('th')]
    table['info']['units'] = [*map(fix_units, map(str.strip, (i.text for i in units.find_all('th'))))]
    table['info']['notes'] = [i.text for i in notes.find('ol').find_all('span', {'class': 'reference-text'})]
    return gatherling

def save(parseling:dict, fname='chemical_elements.json') -> dict:
    with open(fname, 'w') as fob:
        json.dump(parseling, fob, sort_keys=True)
        os.startfile(fname)
    return {fname: parseling}






if __name__ == '__main__':
    uri = 'https://en.wikipedia.org/wiki/List_of_chemical_elements'
    uri = 'List of chemical elements - Wikipedia.html'
    g = gather(uri)
    p = parse(g)
    # print(p)
    s = save(p)
    # print(s)