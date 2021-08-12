from statistics import variance
from itertools import combinations
import io

from sl4ng import diffs

def compare(l1, l2):
    if len(l1) == len(l2):
        discrepancies = [i for i, e in enumerate(l1) if e!=l2[i]]
        print(f"{len(discrepancies) = }")
        print(f"{variance(diffs(discrepancies)) = }\n")
        

with open('unicode_cheatsheet-backslashreplace.txt', mode='r', encoding='utf-8', errors='backslashreplace') as one:
    with open('unicode_cheatsheet-xmlcharrefreplace.txt', mode='r', encoding='utf-8', errors='xmlcharrefreplace') as two:
        with open('unicode_cheatsheet-replace.txt', mode='r', encoding='utf-8', errors='replace') as three:
            
            lines = {
                'backslashreplace': one.readlines()[:],
                'xmlcharrefreplace': two.readlines()[:],
                'replace': three.readlines()[:],
            }
            
            print(*map(len, map(lines.get, lines.keys())))
            print(f"{variance(map(len, map(lines.get, lines.keys()))) = }")
            print()
            for pair in combinations(lines.keys(), 2):
                print('-' * 75, end='\n\n')
                x, y = pair
                print(f"{x} vs {y}")
                pair = map(lines.get, pair)
                compare(*pair)