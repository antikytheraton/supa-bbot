# Algoritmo para detectar mes del anio en interaccion conversacional
# Version: 	1.0
# Autor:	Aaron Arredondo Sanchez
# Fecha: 	16 de Junio de 2017

import difflib
import operator

def mes_filtro(text):
	try:
	    month_dict ={
	    'enero':  		['enero', 'ene', 'january'], 
	    'febrero':  	['febrero', 'feb', 'february'], 
	    'marzo':  		['marzo', 'mar', 'march'], 
	    'abril':  		['abril', 'abr', 'april'], 
	    'mayo':  		['mayo', 'may', 'may'], 
	    'junio':  		['junio', 'jun', 'june'], 
	    'julio':  		['julio', 'jul', 'july'], 
	    'agosto':  		['agosto', 'ago', 'august'], 
	    'septiembre':  	['septiembre', 'sep', 'september'], 
	    'octubre': 		['octubre', 'oct', 'october'], 
	    'noviembre': 	['noviembre', 'nov', 'november'], 
	    'diciembre': 	['diciembre', 'dic', 'december']
	    }

	    month_key = list(month_dict.keys())
	    month_value = list(month_dict.values())

	    month_dict_match = {month_key[i]:difflib.get_close_matches(text, month_value[i]) for i in range(len(month_key))}
	    
	    reduced_month_dict = {k: v for k, v in month_dict_match.items() if v}
	    
	    pct_match = []
	    month_match = {}
	    
	    for i in reduced_month_dict.values():
	        l = difflib.SequenceMatcher(None, text, i[0]).ratio()*100
	        pct_match.append(l)
	        match_dict = {i[0]:l}
	        month_match.update(match_dict)
	        
	    closest_match = max(month_match, key=month_match.get)
	    
	    for month_key, values in month_dict.items():
	        if closest_match in values:
	            return month_key
	
	except:
		return False

def estado_filter(text):
	try:
	    state_dict = {
	    "Aguascalientes":		['aguascalientes'],
		"Baja California":		['baja california', 'tijuana', 'tecate'],
		"Baja California Sur":	['baja california sur', 'la paz', 'los cabos'],
		"Campeche":				['campeche', 'ciudad del carmen'],
		"Chiapas":				['chiapas', 'tuxtla gutierrez','tuxtla' , 'san cristobal de las casas'],
		"Chihuahua":			['chihuahua', 'ciudad juarez', 'juarez'],
		"Coahuila":				['coahuila', 'saltillo'],
		"Colima":				['colima', 'manzanillo'],
		"Ciudad De Mexico":		['ciudad de mexico', 'distrito federal', 'cdmx', 'df', 'chilangolandia'],
		"Durango":				['durango'],
		"Mexico":				['estado de mexico', 'edomex', 'toluca'],
		"Guanajuato":			['guanajuato', 'celaya'],
		"Guerrero":				['guerrero', 'chilpancingo', 'acapulco', 'taxco'],
		"Hidalgo":				['hidalgo', 'tula', 'pachuca', 'cruz azul'],
		"Jalisco":				['jalico', 'guadalajara', 'tequila'],
		"Michoacan":			['michoacan', 'morelia', 'uruapan', 'patzcuaro'],
		"Morelos":				['morelos', 'cuernavaca'],
		"Nayarit":				['nayarit', 'tepic'],
		"Nuevo Leon":			['nuevo leon', 'monterrey'],
		"Oaxaca":				['oaxaca', 'huatulco'],
		"Puebla":				['puebla'],
		"Queretaro":			['queretaro'],
		"Quintana Roo":			['quintana roo', 'cancun'],
		"San Luis Potosi":		['san luis potosi'],
		"Sinaloa":				['sinaloa', 'culiacan', 'guasave', 'mochis'],
		"Sonora":				['sonora', 'hermosillo'],
		"Tabasco":				['tabasco', 'villa hermosa'],
		"Tamaulipas":			['tamaulipas', 'ciudad victoria', 'matamoros', 'reynosa'],
		"Tlaxcala":				['tlaxcala', 'huamantla'],
		"Veracruz":				['veracruz', 'xalapa', 'coatzacoalcos'],
		"Yucatan":				['yucatan', 'merida'],
		"Zacatecas":			['zacatecas']
	    }

	    state_key = list(state_dict.keys())
	    state_value = list(state_dict.values())

	    state_dict_match = {state_key[i]:difflib.get_close_matches(text, state_value[i]) for i in range(len(state_key))}
	    
	    reduced_state_dict = {k: v for k, v in state_dict_match.items() if v}
	    
	    pct_match = []
	    state_match = {}
	    
	    for i in reduced_state_dict.values():
	        l = difflib.SequenceMatcher(None, text, i[0]).ratio()*100
	        pct_match.append(l)
	        match_dict = {i[0]:l}
	        state_match.update(match_dict)
	        
	    closest_match = max(state_match, key=state_match.get)
	    
	    for state_key, values in state_dict.items():
	        if closest_match in values:
	            return state_key
	
	except:
		return False
# while True:
# 	text = input("prueba mes: ")
# 	lower_text = text.lower()
# 	mes = mes_filtro(lower_text)
# 	print(mes)