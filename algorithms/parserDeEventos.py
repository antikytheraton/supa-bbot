from xml.dom import minidom

xmldoc = minidom.parse('XML_Evento.xml')
itemlist = xmldoc.getElementsByTagName('evento')
print(len(itemlist))
print(itemlist[0].attributes['busqueda'].value)

l = []
for s in itemlist:
    print(s.attributes['busqueda'].value)
    # l.append(l)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# from xml.dom import minidom

# xmldoc = minidom.parse('XML_Evento.xml')
# eventlist = xmldoc.getElementsByTagName('evento')
# infolist = xmldoc.getElementsByTagName('informacion')

# for s in infolist:
# 	print(s)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# import xml.etree.ElementTree
# e = xml.etree.ElementTree.parse('XML_Evento.xml').getroot()

# for atype in e.findall('evento'):
#     print(atype.get('busqueda'))