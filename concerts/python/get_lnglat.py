import csv
from bs4 import BeautifulSoup
import urllib2

def dms_to_dd(d, m, s):
    dd = float(d) + float(m)/60 + float(s)/3600
    return dd

def getLngLat(resp):

    coords = []
    soup = BeautifulSoup(resp, "lxml")

    for link in soup.find_all('a', href=True):
        lnk = link['href']
        if("tools.wmflabs.org" in lnk):
            rawCoords = (lnk.split('&params=')[1]).split('W_')[0] + "W"
            #print rawCoords
            if rawCoords not in coords:
                coords.append(rawCoords)

    finalLatLng = []

    if(len(coords) == 0):
        return finalLatLng
    else:
        #print coords[0]
        rawCoord = coords[0]

        rawLat = rawCoords.split("_N_")[0] + "_N"
        lat01 = rawLat.split('_N')
        lat02 = lat01[0]
        arrDMSLat = lat02.split('_')
        #print len(arrDMSLat)

        if len(arrDMSLat) == 1:
            #print arrDMSLat[0]
            finalLatLng.append(float(arrDMSLat[0]))
        elif len(arrDMSLat) == 3:
            #print ararrDMSLatrDMS[0]
            #print arrDMSLat[1]
            #print arrDMSLat[2]
            finalLatLng.append(float(dms_to_dd(arrDMSLat[0], arrDMSLat[1], arrDMSLat[2])))

        rawLng = rawCoords.split("_N_")[1]
        #print rawLng
        lng01 = rawLng.split('_W')
        lng02 = lng01[0]
        arrDMSLng = lng02.split('_')
        #print arrDMSLng
        #print len(arrDMSLng)

        if len(arrDMSLng) == 1:
            #print arrDMSLng[0]
            finalLatLng.append(float(arrDMSLng[0]) * -1)
        elif len(arrDMSLng) == 3:
            #print arrDMSLng[0]
            #print arrDMSLng[1]
            #print arrDMSLng[2]
            finalLatLng.append(float(dms_to_dd(arrDMSLng[0], arrDMSLng[1], arrDMSLng[2]) * -1))

        #print rawLng
        lng01 = rawLng.split('_E')
        lng02 = lng01[0]
        arrDMSLng = lng02.split('_')
        #print arrDMSLng
        #print len(arrDMSLng)

        if len(arrDMSLng) == 1:
            #print arrDMSLng[0]
            finalLatLng.append(float(arrDMSLng[0]))
        elif len(arrDMSLng) == 3:
            #print arrDMSLng[0]
            #print arrDMSLng[1]
            #print arrDMSLng[2]
            finalLatLng.append(float(dms_to_dd(arrDMSLng[0], arrDMSLng[1], arrDMSLng[2])))

        #print finalLatLng

        return finalLatLng

with open('uk_tour_1971.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 0:
            try:
                resp = urllib2.urlopen(row[4])
                lngLat = getLngLat(resp)
                if(len(lngLat) > 0):
                    print (row[4]) + "|" + str(lngLat[0]) + ',' + str(lngLat[1])
                else:
                    print (row[4]) + "|"
            except:
                print (row[4] + "|")

        line_count = line_count + 1


#resp = urllib2.urlopen("https://en.wikipedia.org/wiki/Pavillon_de_Paris")
#print getLngLat(resp)