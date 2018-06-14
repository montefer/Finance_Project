import urllib.request
import requests
import re
import datetime
import time
import csv

def convert_time_from_unix(timestamp):
    date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
    return date


def convert_time_to_unix(timestamp):
    try:
        unix_time = int(time.mktime(datetime.datetime.strptime(timestamp, "%Y-%m-%d").timetuple()))
    except OSError:
        unix_time = int(time.mktime(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").timetuple()))
    return str(unix_time)


def stock_numbers(data):
    data = re.split('(\-\d+\.\d+|\d+\.\d+|^[0-9]*$|\d+)', str(data))
    return [x for x in data if x.isdigit() or re.match("^\d+?\.\d+?$",x)]


ticker = input('Please input stock ticker: ').upper()

period1 = convert_time_to_unix(input('Please input start date (YYYY-MM-DD): '))
period2 = convert_time_to_unix(input('Please input end date (YYYY-MM-DD): '))




page_url = 'https://finance.yahoo.com/quote/'+ticker+'/history?period1='+period1+'&period2='+period2+'&interval=1d&filter=history&frequency=1d'





page = requests.get(page_url)

print(page)
i=0

header = ['Date','Open','High','Low','Close','Volume','Adjusted Close']
split_header = ['Date','Numerator','Denominator','splitRatio','Type']
dividend_header = ['Date','Amount','Type']

with urllib.request.urlopen(page_url) as f:
    html = f.read().decode('utf-8')
    price_table_start = html.find('HistoricalPriceStore')
    price_table_end = html.find('eventsData')


    html = html[price_table_start:price_table_end]
    price_table_start = html.find('prices')
    
    stock_info = html[price_table_start:price_table_end]
    stock_data = re.findall('\{(.*?)\}',stock_info)

    numbers_list = stock_numbers(stock_data)    #will give: date(UNIX timestamp), open, high,
                                                #low, close, volume, adjusted close (in that order)
    #print(numbers_list)

    with open('yahoo_stock_info.csv', 'a') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(header)

        for item in stock_data:
            if "DIVIDEND" in item:
                print('Contains dividend!')
                date = convert_time_from_unix(numbers_list[i+1])
                dividend = [date,numbers_list[i],'DIVIDEND']
                wr.writerow(dividend_header)
                wr.writerow(dividend)
                i+=3





            elif "SPLIT" in item:
                print('Contains stock split!')
                date = convert_time_from_unix(numbers_list[i])
                numerator = numbers_list[i+1]
                denominator = numbers_list[i+2]
                split_ratio = float(numbers_list[i+3])/float(numbers_list[i+5])
                stock_split = [date, numerator, denominator, split_ratio,'SPLIT']
                wr.writerow(split_header)
                wr.writerow(stock_split)
                i+=9



                
            else:           #if re.match("^\d+?\.\d+?$", numbers_list[i+1]) or re.match("^\d+?\.\d+?$", numbers_list[i+2]) or re.match("^\d+?\.\d+?$", numbers_list[i+3]) or re.match("^\d+?\.\d+?$", numbers_list[i+4]):

                date = convert_time_from_unix(numbers_list[i])
                stock_information = numbers_list[i+1:i+7]
                stock_information.insert(0,date)
                wr.writerow(stock_information)
                i+=7    
