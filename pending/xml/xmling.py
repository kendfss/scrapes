import xml.dom.minidom as md
import xml.etree.ElementTree as ET
import xml4h
file = 'sample.xml'
# file = 'menu.xml'
tree = ET.parse(file)
root = tree.getroot()
# print(tree, root)
# tree = md.parse(file)
# tree = xml4h.parse(file)

# for x in root:
    # print(x)
    
for description in root.iter('description'):
    new_desc = str(description.text).strip()+' - will be served'
    description.text = str(new_desc)
    description.set('updated', 'yes')
    tree.write('new.xml')

# for x in root.findall('food'):
# for x in root.iter('food'):
    # print(x)
    # print(x.attrib)
    # help(x)
    
for x in root.findall('food'):
    y = dict(
    item = x.find('item').text,
    price = x.find('price').text,
    description = x.find('description').text.strip(),
    )
    print(y)
# for x in root.findall