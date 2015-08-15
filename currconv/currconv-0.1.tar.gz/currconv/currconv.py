from yahoo_finance import Currency
from argparse import ArgumentParser 
import time

# country numeric codes don't map to EUR for eurozone countries, so 
# need to handle this case separately
eurozone_numeric = ['040', '056', '196', '233', '246', '250', '276', '300', '372', 
'380', '428', '440', '442', '470', '528', '620', '703', '705', '724']

# create argument parser
def get_args():
	parser = ArgumentParser(description='A currency converter for the terminal')

	# positional arguments
	parser.add_argument('amt', metavar='amt', type=float, help='amount to be converted')
	parser.add_argument('b_curr', metavar='b_curr', type=str, help='base currency (ISO 4217 format)')
	parser.add_argument('d_curr', metavar='d_curr', type=str, help='desired currency (ISO 4217 format)')

	# optional arguments
	parser.add_argument('-r', '--rate', action='store_true', help='print exchange rate')
	parser.add_argument('-t', '--time', action='store_true', help='print time of exchange')
	parser.add_argument('-c', '--currency', action='store_true', help='allow currency names in place of \
		ISO 4217 format. (Note: Signficantly slower. ISO 4217 recommended.)')
	parser.add_argument('-n', '--name', action='store_true', help='allow country names in place of \
		ISO 4217 format. (Note: Significantly slower. ISO 4217 recommended.)')

	args = parser.parse_args()
	# put namespace items in dict
	args_dict = vars(args)
	return args_dict

# check whether ISO 4217 Codes present or not
def parse_args(currency_options, names):
	c, n = currency_options
	b_curr, d_curr =  names

	# checks for currency names instead of ISO 4217 codes
	if c:
		# large import, only do so if necessary
		from pycountry import currencies
		# which args are NOT ISO 4217 Codes
		cond1 = not len(b_curr) == 3
		cond2 = not len(d_curr) == 3
		
		# both
		if cond1 and cond2:
			ISO_code = str(currencies.get(name=b_curr).letter)
			b_curr = ISO_code
			ISO_code = str(currencies.get(name=d_curr).letter)
			d_curr = ISO_code
		
		# just base currency
		elif cond1:
			ISO_code = str(currencies.get(name=b_curr).letter)
			b_curr = ISO_code
		
		# just desired currency
		elif cond2:
			ISO_code = str(currencies.get(name=d_curr).letter)
			d_curr = ISO_code


	if n:
		# large import, so only do so if necessary
		from pycountry import countries, currencies
		# which args are NOT ISO 4217 Codes
		cond1 = not len(b_curr) == 3
		cond2 = not len(d_curr) == 3

		# both
		if cond1 and cond2:
			country = countries.get(name=b_curr)
			numeric = str(country.numeric)
			
			if numeric in eurozone_numeric:
				b_curr = 'EUR'
			else:
				ISO_code = str(currencies.get(numeric=numeric).letter)
				b_curr = ISO_code
			
			country = countries.get(name=d_curr)
			numeric = str(country.numeric)
			if numeric in eurozone_numeric:
				d_curr = 'EUR'
			else:
				ISO_code = str(currencies.get(numeric=numeric).letter)
				d_curr = ISO_code

		# just base currency	
		elif cond1:
			country = countries.get(name=b_curr)
			numeric = str(country.numeric)
			if numeric in eurozone_numeric:
				b_curr = 'EUR'
			else:
				ISO_code = str(currencies.get(numeric=numeric).letter)
				b_curr = ISO_code

		# just target currency
		elif cond2:
			country = countries.get(name=d_curr)
			numeric = str(country.numeric)
			if numeric in eurozone_numeric:
				d_curr = 'EUR'
			else:
				ISO_code = str(currencies.get(numeric=numeric).letter)
				d_curr = ISO_code

	return b_curr, d_curr

# performs Yahoo Finance API call, and adds data for display to args dictionary 
def get_rate(args_dict):
	amt = args_dict['amt']
	b_curr = args_dict['b_curr']
	d_curr = args_dict['d_curr']
	c = args_dict['currency']
	n = args_dict['name']
	
	# check whether we need to find ISO 4217 codes
	if c or n:
		currency_options = (c, n)
		names = b_curr, d_curr
		b_curr, d_curr = parse_args(currency_options, names)

	ISO_str = b_curr + d_curr
	# Yahoo Finance API call
	currency = Currency(ISO_str)
	trade_time = currency.get_trade_datetime()
	current_rate = float(currency.get_rate())
	value = amt * current_rate

	# modify args dictionary with data needed for display
	args_dict['b_curr_updated'] = b_curr
	args_dict['d_curr_updated'] = d_curr
	args_dict['value'] = value
	args_dict['current_rate'] = current_rate
	args_dict['trade_time'] = trade_time

	return args_dict

def display(display_dict):
	amt = display_dict['amt']
	b_curr = display_dict['b_curr']
	d_curr = display_dict['d_curr']
	b_curr_updated = display_dict['b_curr_updated']
	d_curr_updated = display_dict['d_curr_updated']
	r = display_dict['rate']
	t = display_dict['time']
	c = display_dict['currency']
	n = display_dict['name']
	value = display_dict['value']
	current_rate = display_dict['current_rate']
	trade_time = display_dict['trade_time']

	# basic functionality
	print('{:.2f} {:} {:10.2f} {:}'.format(amt, b_curr_updated, value, d_curr_updated))
	
	# check whether uses wants current exchange rate
	if r:
		print('{:.2f} {:1} {:12.4f} {:}'.format(1, b_curr_updated, current_rate, d_curr_updated))

	# check whether user wants trade time
	if t:
		print(trade_time)

	# print ISO codes for given currencies (future reference)
	if c:
		cond1 = not b_curr == b_curr_updated
		cond2 = not d_curr == d_curr_updated
		if cond1 and cond2:
			print('The ISO 4217 code for {:} is {:}'.format(b_curr, b_curr_updated))
			print('The ISO 4217 code for {:} is {:}'.format(d_curr, d_curr_updated))
		elif cond1:
			print('The ISO 4217 code for {:} is {:}'.format(b_curr, b_curr_updated))
		elif cond2:
			print('The ISO 4217 code for {:} is {:}'.format(d_curr, d_curr_updated))

	# print ISO codes for given countries (future reference)
	if n:
		cond1 = not (b_curr == b_curr_updated)
		cond2 = not (d_curr == d_curr_updated)
		if cond1 and cond2:
			print('The ISO 4217 code for {:} is {:}'.format(b_curr, b_curr_updated))
			print('The ISO 4217 code for {:} is {:}'.format(d_curr, d_curr_updated))
		elif cond1:
			print('The ISO 4217 code for {:} is {:}'.format(b_curr, b_curr_updated))
		elif cond2:
			print('The ISO 4217 code for {:} is {:}'.format(d_curr, d_curr_updated))
		
def main():
	args_dict = get_args()
	display_dict = get_rate(args_dict=args_dict)
	display(display_dict=display_dict)

if __name__ == "__main__":
	now = time.time()
	main()
	print(time.time() - now)