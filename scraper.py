import requests
from bs4 import BeautifulSoup
import csv

def scrape():
    url = 'https://www.lmsal.com/solarsoft/latest_events_archive.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    links = []
    for link in table.find_all('a'):
        if link.has_attr('href'):
            links.append('https://www.lmsal.com/solarsoft/' + link['href'])

    sp_data = []
    j = 0
    links = links[:200]                                                             # Change this to adjust how many links to go to and fetch data
    for examp in links:
        examp = BeautifulSoup(requests.get(examp).text, 'html5lib')
        sp_table = examp.find_all('table')[-1]
        
        ok = True
        for row in sp_table.find_all('tr'):
            if (ok):
                ok = False
                continue
            i = 0
            sp_data.append([])
            for subrow in row.find_all('td'):
                if i == 0:
                    i += 1
                    print(row)
                    print()
                    continue
                
                sp_data[j].append(subrow.getText().replace('\n', ''))
                i += 1

            print(len(sp_data[j]))
            if j == 10:
                print(sp_data[j])
            j += 1
        
    with open('file1.txt', 'w') as f:
        f.write(str(sp_data))
    
    print(len(sp_data))

    elems = {}
    for row in sp_data:
        if row == []:
            continue
        elems[row[0]] = row

    with open('file2.txt', 'w') as f:
        f.write(str(elems))
    
    final = []
    fields = ['EName', 'Start', 'Stop', 'Peak', 'GOES Class', 'Derived Position']
    for key in elems:
        final.append(elems[key])
    
    with open('file.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        writer.writerows(final)
    


scrape()