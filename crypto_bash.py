import sys, requests, time
 
# api-endpoint 
URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false"

# sending get request and saving the response as response object 
r = requests.get(url = URL) 
  
# extracting data in json format 
data = r.json()

i = 1
arglen = len(sys.argv)
escseq = '\033[' + str(arglen - 1) + 'A'

def findIdByTicker(url, ticker):
	for arr in data:
		if arr['symbol'] == ticker:
			print ('%s\t%s\t%s%%' %(arr['symbol'], arr['current_price'],  arr['price_change_percentage_24h']))
			break;

while i < arglen:
	if sys.argv[i] == '-l':
		i += 1
		while 1:
			if i == arglen:
				r = requests.get(url = URL) 
				data = r.json()
				print escseq
				time.sleep(15)
				i = 1
			TICKER = sys.argv[i]
			findIdByTicker(URL, TICKER)
			i += 1
	else:
		TICKER = sys.argv[i]
		findIdByTicker(URL, TICKER)
		i += 1 
