from json import dump
import re

from sl4ng import splitter, show, pop, getsource, flat

PATH = 'allascii.txt'
INDEX = 11

def cast_number(string):
    try:
        return (float, int)[isint(string)](string)
    except ValueError:
        return int(float(string))

def isint(string):
    string = str(string)
    numeric = all(map(str.isnumeric, splitter('.-')(string)))
    periods = string.count('.')
    negs = string.count('-')
    if periods > 1 or negs > 1 or not numeric:
        raise ValueError
    elif periods == 0:
        return True
    elif not any(map(int, string.split('.')[-1])):
        return True
    return False


def extract(path, index):
    with open(path, 'r') as fob:
        return fob.readlines()[index:]

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
    # if (match := re.search('\w+\^\-\d+', sub)):
    if (match := re.search('\w+\^\-\d+|\((.)+\)\^\-\d+', sub)):
        *dim, power = sub.split('^')
        dim = '^'.join(dim)
        # print(isint(power), power)
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

def parse(path, index):
    text = map(splitter('|'), extract(path, index))
    zipper = (tuple(map(str.strip, i)) for i in map(list, text))
    return {
        name: {
            "value": fix_magnitude(value),
            # "value": (value),
            "uncertainty": fix_magnitude(uncertainty),
            # "uncertainty": (uncertainty),
            "units": fix_units(units),
            # "units": (units),
            "symbol": [],
        }
        for name, value, uncertainty, units in zipper
    }

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



def scrape(path, index, reveal=False):
    outs = "physical_constants.json physical_constants-min.json".split()
    table = parse(path, index)
    for name in outs:
        indent = None if '-min.' in name else '    '
        with open(name, 'w') as fob:
            dump(table, fob, indent=indent, sort_keys=True)
        print(pop(name)) if reveal else False 
    return table


if __name__ == '__main__':
    table = scrape(PATH, INDEX)
    print(f"{len(table) = }")
    planck = table['Planck constant']
    print(f"{planck['value'] = }")
    print(f"{fix_magnitude(planck['value']) = }")
    print(f"{6.62607015 * 10 ** -34 = }")

    # show(units(PATH, INDEX))
    u = sorted(units(PATH, INDEX))
    fixes = [*map(fix_units, u)]
    show(zip(u, fixes))
    show(map(fix_unit_power, fixes))
    # print(all(i.count('/')<=2 for i in fixes))
    # show(filter(lambda i: not i.count('/')<=2, fixes))
    # print(all(isinstance(i, str) for i in fixes))
    # show(filter(lambda i: not isinstance(i, str), fixes))
    check(PATH, INDEX)
    show(values(PATH, INDEX))
    

