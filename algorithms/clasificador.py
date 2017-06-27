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
while True:
	text = input("prueba mes: ")
	lower_text = text.lower()
	mes = mes_filtro(lower_text)
	print(mes)