import urllib.request
with urllib.request.urlopen('https://super-boletos-bot.herokuapp.com/assets/data_events.xml') as f:
	print(f.read())
