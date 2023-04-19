from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

table_file = "table.txt"

######
def normalize(x, x_min, x_max):
    if x_max == x_min: return 0
    y = (x - x_min) / (x_max - x_min)
    return y

with open(table_file) as fp:
    soup = BeautifulSoup(fp, 'html.parser')

row_list = soup.find_all('button', {'class' : 'btn btn-light btn-sm'})

key_list = []
for r in range(0, 65*3, 3):
    range = row_list[r]['data-clipboard-text']
    private_key = row_list[r+1]['data-clipboard-text']
    address = row_list[r+2]['data-clipboard-text']

    key_list.append([range, private_key, address])

li = []
nor = []
for i in key_list:
    range_str = i[0]
    range_min, range_max = range_str.split(':')
    int_range_min = int(range_min, 16)
    int_range_max = int(range_max, 16)
    int_pvkey = int(i[1], 16)
    norm = normalize(int_pvkey, int_range_min, int_range_max)

    print(0, norm, 1)
    li.append([int_range_min, int_pvkey, int_range_max])
    nor.append(norm)

plt.plot(nor, 'x')
plt.show()

plt.plot(nor)
plt.show()

import csv


with open('sample.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    for i in li:
        print(i)
        # write the header
        #writer.writerow(i)




