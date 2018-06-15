import csv

with open('wayback_clean.csv','r') as quarters:
    quarter_indices = dict((r[0],i) for i, r in enumerate(csv.reader(quarters)))

print(quarter_indices)    
with open('yahoo_stock_info.csv', 'r') as yahoo_stock:
    with open('merged_files.csv', 'w', newline='') as merged:
        reader = csv.reader(yahoo_stock)
        writer = csv.writer(merged)

        writer.writerow(next(reader, []) + ['RESULTS'])

        #for row in reader:
        #    index = quarter_indices.get(row[0])
        #    if index is not None:
        #        message = 'FOUND in quarters list (row {})'.format(index)
        #    else:
        #        message = 'NOT found in quarters list'
        #    writer.writerow(row + [message])

        for row in reader:
            index = quarter_indices.get(row[0])
            if index is not None:
                message = 'FOUND in quarters list (row {})'.format(index)
                writer.writerow(row + [message])
            else:
                #print('NOT found in quarters list')
                pass
