import sys, requests, time

# api-endpoint 
URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false"

def main():
	i = 1
	arglen = len(sys.argv)
	escseq = '\033[' + str(arglen - 1) + 'A'

	data = parsing()
	while i < arglen:
		if sys.argv[i] == '-l':
			i += 1
			while 1:
				if i == arglen:
					data = parsing()
					print escseq
					time.sleep(15)
					i = 1
				TICKER = sys.argv[i]
				findIdByTicker(URL, TICKER, data)
				i += 1
		else:
			TICKER = sys.argv[i]
			findIdByTicker(URL, TICKER, data)
			i += 1 

def parsing():
	request = requests.get(url = URL) 
	data = request.json()
	return data

def findIdByTicker(url, ticker, data):
	for arr in data:
		if arr['symbol'] == ticker:
			print ('%s\t%s\t%s%%' %(arr['symbol'], arr['current_price'],  arr['price_change_percentage_24h']))
			break;

if __name__ == "__main__":
    main()