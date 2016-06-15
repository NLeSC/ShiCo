from BeautifulSoup import BeautifulSoup
import re
import nltk
import string
from HTMLParser import HTMLParser

# Helper functions

def getText(textElement):
    regex = re.compile('\ +')
    html = HTMLParser()

    text = regex.sub(' ', textElement)
    text = text.strip()
    text = html.unescape(text)

    return text

def getTitle(article):
    title = article.find('text.title')
    if title is None:
        return ''
    titleText = title.getText(' ')
    return getText(titleText)

def getBody(article):
    crs = article.findAll('text.cr')
    crTexts = [ getText(cr.getText(' ')) for cr in crs ]
    return ' '.join(crTexts)

def getSoupFromXML(xmlfile):
    with open(datafile,'r') as fin:
        data = fin.read()
    soup = BeautifulSoup(data)
    return soup

def getArticlesFromSoup(soup):
    articles = []
    for article in soup.findAll('article'):
        title = getTitle(article)
        body = getBody(article)
        articles.append((title, body))
    return articles

# Example file load
# datafile = 'data/times-20101217/0FFO-2010-1217.xml'
# soup = getSoupFromXML(datafile)
# articles = getArticlesFromSoup(soup)
# print len(articles)
# title, body = articles[100]
# print 'Title  :',title
# print 'Content:\n', body

# ## Load XML and save as CSV
from glob2 import glob
import pandas as pd
import os

origPath = 'TDA_GDA/TDA_2010/'
savePath = 'myTimes/'

# Save / load as CSV
for datafile in glob(origPath + '**/0FFO*.xml'):
    print 'Loading   : ',datafile
    saveFile = savePath + os.path.basename(datafile)
    saveFile = saveFile.replace('.xml', '.csv')
    print '...save as: ',saveFile

    soup = getSoupFromXML(datafile)
    articles = getArticlesFromSoup(soup)

    df = pd.DataFrame(articles, columns=['Title', 'Content'])
    df.to_csv(saveFile, encoding='UTF8')

