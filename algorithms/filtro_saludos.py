def saludos_filtro(text):
	try:
	    sal_des_dict ={
	    'hola':  		['hola', 'holi', 'hola bot', ''],
	    'adios':		['']
	    }

	    month_key = list(sal_des_dict.keys())
	    month_value = list(sal_des_dict.values())

	    sal_des_dict_match = {month_key[i]:difflib.get_close_matches(text, month_value[i]) for i in range(len(month_key))}
	    
	    reduced_sal_des_dict = {k: v for k, v in sal_des_dict_match.items() if v}
	    
	    pct_match = []
	    month_match = {}
	    
	    for i in reduced_sal_des_dict.values():
	        l = difflib.SequenceMatcher(None, text, i[0]).ratio()*100
	        pct_match.append(l)
	        match_dict = {i[0]:l}
	        month_match.update(match_dict)
	        
	    closest_match = max(month_match, key=month_match.get)
	    
	    for month_key, values in sal_des_dict.items():
	        if closest_match in values:
	            return month_key
	
	except:
		return False