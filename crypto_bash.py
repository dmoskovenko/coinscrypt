import sys, requests, time

# api-endpoint 
URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false"

# colored output
RED='\033[0;31m'
GREEN='\033[0;32m'
GRAY='\033[1;30m'
NC='\033[0m'

def main():
	i = 1
	arglen = len(sys.argv)
	escseq = '\033[' + str(arglen - 1) + 'A'
	data = parsing()
	header = '{:s}{:<12s}{:<12s}{:s}{:s}'.format(GRAY, 'Name', 'Price', '%24h', NC)

	print header
	while i < arglen:
		if sys.argv[i] == '-l':
			i += 1
			while 1:
				if i == arglen:
					data = parsing()
					print escseq
					time.sleep(15)
					i = 1
				printCoins(URL, data, i)
				i += 1
		else:
			printCoins(URL, data, i)
			i += 1 

def parsing():
	request = requests.get(url = URL) 
	data = request.json()
	return data

def printCoins(url, data, i):
	ticker = sys.argv[i]

	for arr in data:
		if arr['symbol'] == ticker:
			if arr['price_change_percentage_24h'] > 0:
				color = GREEN
				sign = "+"
			else:
				color = RED
				sign = ""
			print ('{:<12s}{:<12s}{:s}{:+.2f}%{:s}'.format(arr['symbol'], str(arr['current_price']), color, arr['price_change_percentage_24h'], NC))
			break;

if __name__ == "__main__":
    main()
