import csv
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib2
import re

def dms_to_dd(d, m, s):
    dd = float(d) + float(m)/60 + float(s)/3600
    return dd

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

with open('uk_tour_1971.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 0:
            try:
                resp = urllib2.urlopen(row[4])
                text_only = text_from_html(resp).lower()
                cap = getPossibleCapacitiesFrom(text_only)
                print (row[4]) + "|" + str(cap)
            except:
                print (row[4] + "|")
                
        line_count = line_count + 1