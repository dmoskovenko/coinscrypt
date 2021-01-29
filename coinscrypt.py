import sys, requests, time

# api-endpoint 
URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=1h%2C7d"

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
	header = '{:s}{:<6s}{:<8s}{:<12s}{:<10s}{:<10s}{:<10s}{:<16s}{:s}{:s}'.format(GRAY, 'Rank', 'Ticker', 'Price', '1h', '24h', '7d', '24h Volume', 'Market Cap', NC)

	print header
	while i < arglen:
		if sys.argv[i] == '-l':
			i += 1
			while 1:
				if i == arglen:
					data = parsing()
					print escseq
					time.sleep(60)
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
			color1h = GREEN if arr['price_change_percentage_1h_in_currency'] > 0 else RED
			color24h = GREEN if arr['price_change_percentage_24h'] > 0 else RED
			color7d = GREEN if arr['price_change_percentage_7d_in_currency'] > 0 else RED
			print ('{:<6d}{:<8s}{:<12s}{:s}{:<+10.2%}{:s}{:<+10.2%}{:s}{:<+10.2%}{:s}{:<16,d}{:,d}'.format(arr['market_cap_rank'], arr['symbol'].upper(), str(arr['current_price']), color1h, (arr['price_change_percentage_1h_in_currency']/100), color24h, (arr['price_change_percentage_24h']/100), color7d, (arr['price_change_percentage_7d_in_currency']/100), NC, arr['total_volume'], arr['market_cap']))
			break;

if __name__ == "__main__":
    main()
