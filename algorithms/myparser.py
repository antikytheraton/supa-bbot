from xml.dom import minidom

xmldoc = minidom.parse('movies.xml')
itemlist = xmldoc.getElementsByTagName('movie')
print(len(itemlist))
print(itemlist[0].attributes['title'].value)
for s in itemlist:
    print(s.attributes['title'].value)