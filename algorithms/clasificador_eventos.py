import xml.etree.ElementTree
import difflib
import random

def event_filter(text):
	# Aqui ocupo importo y parseo el archivo XML
	f = open("XML_Eventos.xml","rb")
	e = xml.etree.ElementTree.parse(f).getroot()

	# Aqui armo el diccionario con todos los datos relevantes de los eventos
	listoflists = []
	dictio = {}
	l = []
	d = {}
	i = 1
	for atype in e.findall('evento'):
		if 'CANCELADO' not in atype.get('estatus_venta'):
			listoflists.append(atype.get('nombre'))
			l.append([atype.get('nombre'),atype.get('recinto'),atype.get('ciudad'),atype.get('clave_tipo'),[atype.get('fechas')]])
			dictio = {atype.get('busqueda'):[atype.get('nombre'),atype.get('recinto'),atype.get('ciudad'),atype.get('clave_tipo')]}
			d.update(dictio)
			i += 1

	# Aqui creo dos listas a partir de mi diccionario, una con las keys y la otra con los values
	event_key = list(d.keys())
	event_val = list(d.values())

	# Aqui contruyo un diccionario de coincidencias
	event_match = {event_key[i]:difflib.get_close_matches(text, event_val[i]) for i in range(len(event_key))}

	# Aqui elimino todos elementos que no coincidieron con la busqueda
	reduct_event_match = {k: v for k, v in event_match.items() if v}

	# Aqui revuelvo mi diccionario
	shuffle_keys = list(reduct_event_match.keys())
	random.shuffle(shuffle_keys)
	random_dict = {shuffle_keys[i]:reduct_event_match.values() for i in range(len(reduct_event_match))}

	# Aqui solo extraigo los primeros 10 elementos
	gd = {}
	gallery_dictio = {}
	gallery_limit = 1
	gallery_key = []
	gallery_val = []
	for key in random_dict:
		if gallery_limit < 11:
			gd = {key:d[key]}
			gallery_dictio.update(gd)
			gallery_limit += 1

	return gallery_dictio


# while True:
# 	evento = input('que evento desea buscar?: ')
# 	eventos = event_filter(evento.upper())
# 	evento_key = list(eventos.keys())
# 	evento_val = list(eventos.values())
# 	evento_tupla = [evento_key, evento_val]
# 	print(evento_tupla)
# 	print(len(evento_key))
	# print(len(eventos.items()))