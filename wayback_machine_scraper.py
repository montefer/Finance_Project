import requests
import urllib.request
import re
import csv
from more_itertools import unique_everseen

# Python code to remove duplicate elements
def Remove(duplicate):
    split_list = []
    for item in duplicate:
        if item not in split_list:
            split_list.append(item)
    return split_list



stock = input("Input the stock ticker you'd like NASDAQ earnings report for: \n").lower()
stock_url = 'https://www.nasdaq.com/earnings/report/'+stock
timestamp = 201812


#page = requests.get('http://archive.org/wayback/available?url='+stock_url+'&timestamp='+str(timestamp))
#print(page.json())
#page_url = page.json()['archived_snapshots']['closest']['url']
#print('\nClosest Url Snapshot:',page_url,'\n')

def get_eps_data(timestamp):
    while timestamp>=201000:

        page = requests.get('http://archive.org/wayback/available?url='+stock_url+'&timestamp='+str(timestamp))
        #print(page.json())
        page_url = page.json()['archived_snapshots']['closest']['url']
        #print('\nClosest Url Snapshot:',page_url,'\n')


        
        with urllib.request.urlopen(page_url) as f:
            html = f.read().decode('utf-8')
            table_title = html.find('Quarterly')
    
            eps_table = html[table_title+350:table_title+2100]
            split_table = re.split('<|>| ',eps_table)

            numbers = []
            dates = []

            j=0

            for num in split_table:
                if re.findall('\-\d+\.\d+|\d+\.\d+|^[0-9]*$',num):
                    numbers.append(re.findall('\-\d+\.\d+|\d+\.\d+|^[0-9]*$',num)[0])
                    j+=1

            for date in split_table:
                if re.findall('\d+/\d+/\d+',date):
                    dates.append(re.findall('\d+/\d+/\d+',date)[0])

            numbers = list(filter(None, numbers))

        
            numbers=numbers[0:12]
            i=0

            if len(numbers)==12:
                with open('wayback_test.csv', 'a') as myfile:
                    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                    for date in dates:
                        eps_info = numbers[i:i+3]
                        eps_info.insert(0,date)
                        wr.writerow(eps_info)
                        i+=3
            else:
                with open('wayback_test.csv', 'a') as myfile:
                    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                    for date in dates:
                        wr.writerow([date])
                        
            if timestamp%100>0:
                timestamp-=3
            else:
                timestamp-=88

            #print(dates)

def del_dup_rows(file):
    with open(file,'r') as f, open('wayback_clean.csv','w') as out_file:
        out_file.writelines(unique_everseen(f))


get_eps_data(timestamp)
del_dup_rows('wayback_test.csv')





    

