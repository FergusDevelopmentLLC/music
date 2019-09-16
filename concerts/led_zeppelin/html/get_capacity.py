import csv
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib2
import re

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

    #print coords
    #print coords[0]
    rawCoord = coords[0]

    rawLat = rawCoords.split("_N_")[0] + "_N"
    lat01 = rawLat.split('_N')
    lat02 = lat01[0]
    arrDMSLat = lat02.split('_')
    #print len(arrDMSLat)

    finalLatLng = []

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

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    stripped = u" ".join(t.strip() for t in visible_texts)
    return re.sub(' +', ' ', stripped)

def getPossibleCapacitiesFrom(text_only):
    
    arrPossibileCaps = []

    if("capacity" in text_only):
        #print "contains capacity"
        words = text_only.split()
        showNextDigit = False
        
        for s in words:
            word = s.replace(",", "")
            if(word == "capacity"):
                showNextDigit = True
            if(showNextDigit and word.isdigit() and int(word) > 2019):
                arrPossibileCaps.append(word)
                showNextDigit = False

    return arrPossibileCaps

with open('1970SummerNorthAmericanTour.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 0:
            resp = urllib2.urlopen(row[4])
            text_only = text_from_html(resp).lower()
            cap = getPossibleCapacitiesFrom(text_only)
            print (row[4]) + "|" + str(cap)
        line_count = line_count + 1