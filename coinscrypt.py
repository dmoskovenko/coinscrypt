import sys
import os
import time
import json
if sys.version_info[0] == 3:
	from urllib.request import urlopen
else:
	from urllib import urlopen

# api-endpoint 
URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=1h%2C7d"

# colors
RED='\033[0;31m'
GREEN='\033[0;32m'
GRAY='\033[1;30m'
NC='\033[0m' # No color

# options
UPDATE_MODE = False
TOP = 0
WRONG_OPTION = ''

def main():
	arg_len = len(sys.argv)
	tickers = arg_parsing(arg_len)
	columns = get_screen_size()

	if UPDATE_MODE is True:
		while True:
			str_count = print_controller(url_parsing(), tickers, columns)
			print('\033[2A')
			time.sleep(15)
			print('\033[' + str(str_count) + 'A')
	# elif TOP > 0:
	# 	if (element['market_cap_rank'] is None or element['symbol'] is None or element['current_price'] is None or element['price_change_percentage_1h_in_currency'] is None or element['price_change_percentage_24h'] is None or element['price_change_percentage_7d_in_currency'] is None or element['total_volume'] or element['market_cap'] is None):
	# 		continue
	else:
		print_controller(url_parsing(), tickers, columns)

def arg_parsing(arg_len):
	global UPDATE_MODE
	global TOP
	global WRONG_OPTION
	tickers = []
	i = 1

	while i < arg_len:
		if sys.argv[i][0] == '-':
			if len(sys.argv[i]) == 2:
				if sys.argv[i][1] == 'u':
					UPDATE_MODE = True
				elif sys.argv[i][1] == 't':
					if sys.argv[i + 1].isdigit():
						tickers.append(sys.argv[i])
						TOP = int(sys.argv[i + 1])
				elif WRONG_OPTION == '':
					WRONG_OPTION = sys.argv[i]
			elif WRONG_OPTION == '':
					WRONG_OPTION = sys.argv[i]
		elif sys.argv[i].isdigit() is False:
			tickers.append(sys.argv[i])
		i += 1
	return tickers

def get_screen_size():
    rows, columns = os.popen('stty size', 'r').read().split()
    return (columns)

def url_parsing():
	response = urlopen(URL)
	data = json.loads(response.read())
	return data

def print_controller(data, tickers, columns):
	top_splitter = False
	no_option_splitter = False
	str_count = 0
	
	if tickers:
		if WRONG_OPTION != '':
			str_count += print_error()
		str_count += print_splitter(columns)
		str_count += print_header()
		str_count += print_splitter(columns)
		for ticker in tickers:
			for element in data:
				if (ticker == '-t') and (TOP > 0):
					if no_option_splitter is True:
						str_count += print_splitter(columns)
						no_option_splitter = False
					str_count += print_coin(element)
					if element['market_cap_rank'] == TOP:
						top_splitter = True
						str_count += print_splitter(columns)
						break
				else:
					if top_splitter is True:
						top_splitter = False
					if element['symbol'] == ticker:
						no_option_splitter = True
						str_count += print_coin(element)
	if not top_splitter is True:
		str_count += print_splitter(columns)
	str_count += print_current_time()
	return str_count

def print_error():
	print('{:s}{:s}'.format('Illegal option ', WRONG_OPTION))
	print('Usage: coin [-u] [-t num] [ticker]')
	return 2

def print_splitter(columns):
	for _ in '_':
		print('{:s}{:s}{:s}'.format(GRAY, _ * int(columns), NC))
	return 1

def print_header():
	header = '{:s}{:<6s}{:<8s}{:<12s}{:<10s}{:<10s}{:<10s}{:<17s}{:s}{:s}'.format(GRAY, 'Rank', 'Ticker', 'Price', '1h', '24h', '7d', '24h Volume','Market Cap', NC)
	print(header)
	return 1

def print_current_time():
	time_float = time.time()
	time_str = time.strftime('%d %b %Y %H:%M:%S %Z', time.localtime(time_float))
	print('{:s}{:s}{:s}'.format(GRAY, time_str, NC))
	return 1

def print_coin(element):
	colors = wich_color(element)
	#print(element['price_change_percentage_1h_in_currency'])
	print('{:<6d}{:<8s}{:<12s}{:s}{:<+10.2%}{:s}{:<+10.2%}{:s}{:<+10.2%}{:s}{:<17,.0f}{:,.0f}'
		.format(element['market_cap_rank'], element['symbol'].upper(), str(element['current_price']),
		colors['1h'], (element['price_change_percentage_1h_in_currency']/100), colors['24h'],
		(element['price_change_percentage_24h']/100), colors['7d'], (element['price_change_percentage_7d_in_currency']/100),
		NC, element['total_volume'], element['market_cap']))
	return 1

def wich_color(element):
	colors = {'1h': NC, '24h': NC, '7d': NC}
	colors['1h'] = GREEN if element['price_change_percentage_1h_in_currency'] >= 0 else RED
	colors['24h'] = GREEN if element['price_change_percentage_24h'] >= 0 else RED
	colors['7d'] = GREEN if element['price_change_percentage_7d_in_currency'] >= 0 else RED
	return colors

if __name__ == "__main__":
    main()
