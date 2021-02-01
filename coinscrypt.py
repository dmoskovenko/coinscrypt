import sys
import json
import urllib
import time
#import requests

# api-endpoint 
URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=1h%2C7d"

# colored output
RED='\033[0;31m'
GREEN='\033[0;32m'
GRAY='\033[1;30m'
NC='\033[0m' # No color

def main():
	i = 1
	arg_len = len(sys.argv)
	esc_seq = '\033[' + str(arg_len - 1) + 'A'
	data = parsing()
	header = '{:s}{:<6s}{:<8s}{:<12s}{:<10s}{:<10s}{:<10s}{:<17s}{:s}{:s}'.format(GRAY, 'Rank', 'Ticker', 'Price', '1h', '24h', '7d', '24h Volume', 'Market Cap', NC)

	print (header)
	while i < arg_len:
		if sys.argv[i] == '-l':
			i += 1
			while True:
				if i == arg_len:
					data = parsing()
					print (esc_seq)
					time.sleep(15)
					i = 1
				print_coins(URL, data, i)
				i += 1
		elif sys.argv[i] == '-t':
			for arr in data:
				if not sys.argv[i + 1].isdigit():
					i += 1
					print ('\n\n')
					break
				#if (arr['market_cap_rank'] is None or arr['symbol'] is None or arr['current_price'] is None or arr['price_change_percentage_1h_in_currency'] is None or arr['price_change_percentage_24h'] is None or arr['price_change_percentage_7d_in_currency'] is None or arr['total_volume'] or arr['market_cap'] is None):
				#	continue
				color_1h = GREEN if arr['price_change_percentage_1h_in_currency'] > 0 else RED
				color_24h = GREEN if arr['price_change_percentage_24h'] > 0 else RED
				color_7d = GREEN if arr['price_change_percentage_7d_in_currency'] > 0 else RED
				print ('{:<6d}{:<8s}{:<12s}{:s}{:<+10.2%}{:s}{:<+10.2%}{:s}{:<+10.2%}{:s}{:<17,d}{:,d}'.format(arr['market_cap_rank'], arr['symbol'].upper(), str(arr['current_price']), color_1h, (arr['price_change_percentage_1h_in_currency']/100), color_24h, (arr['price_change_percentage_24h']/100), color_7d, (arr['price_change_percentage_7d_in_currency']/100), NC, arr['total_volume'], arr['market_cap']))
				if arr['market_cap_rank'] == int(sys.argv[i + 1]):
					i += 1
					break
		else:
			print_coins(URL, data, i)
			i += 1

def parsing():
	response = urllib.urlopen(URL)
	data = json.loads(response.read())
	#data = request.json()
	return data

def print_coins(url, data, i):
	ticker = sys.argv[i]

	for arr in data:
		if arr['symbol'] == ticker:
			color_1h = GREEN if arr['price_change_percentage_1h_in_currency'] >= 0 else RED
			color_24h = GREEN if arr['price_change_percentage_24h'] >= 0 else RED
			color_7d = GREEN if arr['price_change_percentage_7d_in_currency'] >= 0 else RED
			print ('{:<6d}{:<8s}{:<12s}{:s}{:<+10.2%}{:s}{:<+10.2%}{:s}{:<+10.2%}{:s}{:<17,d}{:,d}'.format(arr['market_cap_rank'], arr['symbol'].upper(), str(arr['current_price']), color_1h, (arr['price_change_percentage_1h_in_currency']/100), color_24h, (arr['price_change_percentage_24h']/100), color_7d, (arr['price_change_percentage_7d_in_currency']/100), NC, arr['total_volume'], arr['market_cap']))
			break

if __name__ == "__main__":
    main()
