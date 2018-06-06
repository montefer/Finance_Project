import urllib.request
import requests
import re
import datetime


def convert_time(timestamp):
    print(datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))


def stock_numbers(data):
    data = re.split('(\-\d+\.\d+|\d+\.\d+|^[0-9]*$|\d+)', str(data))
    return [x for x in data if x.isdigit() or re.match("^\d+?\.\d+?$",x)]

page_url = 'https://finance.yahoo.com/quote/GOOG/history?period1=1370404800&period2=1528171200&interval=1d&filter=history&frequency=1d'

page = requests.get(page_url)

print(page)

with urllib.request.urlopen(page_url) as f:
    html = f.read().decode('utf-8')
    price_table_start = html.find('HistoricalPriceStore')
    price_table_end = html.find('eventsData')
    stock_info =html[price_table_start:price_table_end]
    stock_data = re.findall('\{(.*?)\}',stock_info)

    numbers_list = stock_numbers(stock_data[0:2])   #will give: date(UNIX timestamp), open, high,
                                                        #low, close, adjusted close, volume (in that order)
    print(numbers_list)

    
