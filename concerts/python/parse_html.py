from bs4 import BeautifulSoup
import urllib2

soup = BeautifulSoup(open("uk_tour_1971.html"), "html.parser")

tables = soup.findChildren('table')

my_table = tables[0]
rows = my_table.findChildren(['th', 'tr'])
for row in rows:
    cells = row.findChildren('td')
    rowString = ""
    delim = ""
    i = 1
    for cell in cells:
        rowString = rowString + delim + str(cell.string)
        if i == 4:
            links = cell.findChildren('a')
            if(len(links) > 0):
                rowString = rowString + delim + links[0]['href']
        delim = "|"
        i=i+1
    print(rowString)
        