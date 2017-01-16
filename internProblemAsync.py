import urllib.request, json, asyncio, aiohttp
from math import ceil

'''
Shopify Summer Internship 2017 Application problem
The task was to use the Shopify API endpoints given and 
write a program to add up the orders for a shopify store 
to get the total revenue for the store. The revenue is displayed
in the terminal in both CAD and USD.

This is my second version, it accomplishes the task with asynchronous
calls to the API and is faster than the first version. I was unhappy with
the first version's efficiency so I learned how to do implement an async
solution in Python.

Author: James Thibaudeau
'''
	
base_orders_URL='https://shopicruit.myshopify.com/admin/orders.json?status=paid&page=1&limit=50&fields=total_price,total_discounts,total_price_usd,total_tax&access_token=c32313df0d0ef512ca64d5b336a0d7c6'
base_count_URL='https://shopicruit.myshopify.com/admin/orders/count.json?status=paid&access_token=c32313df0d0ef512ca64d5b336a0d7c6'
limit = 50
fields = {'total_price': 0, 'total_price_usd':0}
tasks = []

def get_num_pages(limit, count):
	return ceil(count/limit)

def sum_data(data, field):
	return sum((float(item[field])) for item in data)

def get_count(url, field):
	URLData = urllib.request.urlopen(url)
	read = URLData.read()
	data = json.loads(read.decode('utf-8'))
	return data[field]

async def get_order_data(client, url, fields, page_name):
	async with client.get(url) as response:
		return await response.json()

async def sum_order_data(client, url, fields, page_name):
	data = await get_order_data(client, url, fields, page_name)
	
	for field in fields:
		fields[field] += sum_data(data[page_name], field)

def task_gen(client, pages, url, page_name, fields):
	task_list = []
	
	for page in range(pages):
		url = url.replace(('page=' + str(page)), ('page=' + str(page+1)))
		task = asyncio.ensure_future(sum_order_data(client, url, fields, page_name))
		task_list.append(task)
		
	return task_list

def display_totals(totals):
	print("Total Revenue: $" + "%0.2f" % totals['total_price'])
	print("Total Revenue(USD): $" + "%0.2f" % totals['total_price_usd'])

def start(field1, field2):	
	count = get_count(base_count_URL, field1)
	pages = get_num_pages(limit, count)
	
	loop = asyncio.get_event_loop()  
	client = aiohttp.ClientSession(loop=loop)
	
	tasks = task_gen(client, pages, base_orders_URL, field2, fields)
	loop.run_until_complete(asyncio.gather(*tasks))
	client.close()
	display_totals(fields)

# start('count', 'orders')


