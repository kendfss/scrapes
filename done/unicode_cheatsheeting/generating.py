r = int('0x10ffff', 16)

name, ext = 'unicode_cheatsheet txt'.split()
errors = 'backslashreplace xmlcharrefreplace replace'.split()
files = [open(name + '-' + error + '.' + ext, mode='w', encoding='utf-8', errors=error) for error in errors]

for fob in files:
    for i in range(r + 1):
        spaces = (len(str(r))-len(str(i))) * ' '
        line = f"{i}:{spaces+'  '}\t\t{chr(i)}"
        fob.write(line+'\n')
    fob.close()