import urllib.request, json
from math import ceil

'''
Shopify Summer Internship 2017 Application problem
The task was to use the Shopify API endpoints given and 
write a program to add up the orders for a shopify store 
to get the total revenue for the store. The revenue is displayed
in the terminal in both CAD and USD.

This was my first version, it accomplishes the task with synchronous
calls to the API and is not nearly as fast as the async version.

Author: James Thibaudeau
'''

base_orders_URL='https://shopicruit.myshopify.com/admin/orders.json?status=paid&page=1&limit=50&fields=total_price,total_price_usd&access_token=c32313df0d0ef512ca64d5b336a0d7c6'
base_count_URL='https://shopicruit.myshopify.com/admin/orders/count.json?status=paid&access_token=c32313df0d0ef512ca64d5b336a0d7c6'
fields = {'total_price': 0, 'total_price_usd':0}
limit = 50

def get_num_pages(limit, count):
	return ceil(count/limit)

def get_order_data(url, field):
	URLData = urllib.request.urlopen(url)
	read = URLData.read()
	data = json.loads(read.decode('utf-8'))
	return data[field]

def sum_data(data, field):
	return sum((float(item[field])) for item in data)	

def sum_all_pages(num_pages, url, page_name, fields):
	data = []
	totals = fields
	
	for page in range(num_pages):
		url = url.replace(('page=' + str(page)), ('page=' + str(page+1)))
		data = get_order_data(url, page_name)
		
		for field in fields:
			totals[field] += sum_data(data, field)

	return totals
	
def display_totals(totals):
	print("Total Revenue: $" + "%0.2f" % totals['total_price'])
	print("Total Revenue(USD): $" + "%0.2f" % totals['total_price_usd'])
	
def start(field1, field2):
	
	count = get_order_data(base_count_URL, field1)
	pages = get_num_pages(limit, count)
	sum = sum_all_pages(pages, base_orders_URL, field2, fields)
	display_totals(sum)

# start('count', 'orders')










