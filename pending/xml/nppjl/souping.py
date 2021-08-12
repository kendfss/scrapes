import os
from bs4 import BeautifulSoup
from sl4ng import flatten, gather, show, delevel
        
def attrs(file,fundamental='keyword'):
    with open(file,'rb') as fob:
        soup = BeautifulSoup(fob,'lxml')
        attributes = flatten(kw.attrs.keys() for kw in soup.find_all(fundamental))
        return set(attributes)
def names(file):
    with open(file,'rb') as fob:
        soup = BeautifulSoup(fob,'lxml')
        tags = soup.find_all()
        return {i.name for i in tags}        
def themestructure(file):
    with open(file,'rb') as fob:
        soup = BeautifulSoup(fob,'lxml')
        attributes = flatten(kw.attrs.keys() for kw in soup.find_all('keyword'))
        return set(attributes)
def attrstructures(table):
    for k,v in table.items():
        with open(v,'w') as fob:
            for n in names(k):
                print(n,file=fob)
                show(attrs(k,n),1,file=fob)
        os.startfile(v)


langs = tuple(gather(r'C:\Program Files (x86)\notepadpp.7.8.5.bin\autoCompletion',names=False,walk=False))
themes = tuple(gather(r'C:\Program Files (x86)\notepadpp.7.8.5.bin\themes',names=False,walk=False))

l = 'python.xml'
t = 'obsidian.xml'

show(names(l))
show(names(t))

show(attrs(l))
show(attrs(t))

attrtable = {
    'obsidian.xml':'themeAttrStructures.txt',
    'python.xml':'langAttrStructures.txt'
}

