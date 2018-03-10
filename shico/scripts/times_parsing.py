import re
from HTMLParser import HTMLParser
from lxml import etree
from bs4 import BeautifulSoup

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
    with open(xmlfile,'r') as fin:
        data = fin.read()
    soup = BeautifulSoup(data, "lxml-xml")
    return soup

def getArticlesFromSoup(soup):
    articles = []
    for article in soup.findAll('article'):
        title = getTitle(article)
        body = getBody(article)
        articles.append((title, body))
    return articles

def getTitle_fast(article):
    title = article.find('.//text.title')
    if title is None:
        return ''
    titleText = etree.tostring(title, method='text', encoding='unicode')
    return getText(titleText)

def getBody_fast(article):
    crs = article.findall('.//text.cr')
    crTexts = [ getText(etree.tostring(cr, method='text', encoding='unicode')) for cr in crs ]
    return ' '.join(crTexts)

def getSoupFromXML_fast(xmlfile):
    return etree.parse(xmlfile)

def getArticlesFromSoup_fast(soup):
    articles = []
    for article in soup.findall('article'):
        title = getTitle_fast(article)
        body = getBody_fast(article)
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

# origPath = 'mnt/times/TDA_GDA/TDA_GDA_1785-2009/'
origPath = './'
# yearFiles.txt created as:
#   ```ls ./mnt/times/TDA_GDA/TDA_GDA_1785-2009/ > yearFiles.txt```
with open('yearFiles.txt', 'r') as fin:
    yearFiles = fin.readlines()
    yearFiles = [ year.strip() for year in yearFiles ]
savePath = 'myTimes/'

# Save / load as CSV
for year in yearFiles:
    yearPath = origPath + year
    print 'YearPath: ',yearPath
    for datafile in glob(yearPath + '/**/0FFO*.xml'):
        print 'Loading   : ',datafile

        yearDir = savePath + year + '/'

        if not os.path.exists(yearDir):
            print 'create ',yearDir
            os.makedirs(yearDir)

        saveFile = yearDir + os.path.basename(datafile)
        saveFile = saveFile.replace('.xml', '.csv')

        if not os.path.exists(saveFile):
            print '...save as: ',saveFile

            soup = getSoupFromXML_fast(datafile)
            articles = getArticlesFromSoup_fast(soup)

            df = pd.DataFrame(articles, columns=['Title', 'Content'])
            df.to_csv(saveFile, encoding='UTF8')

            del soup
            del articles
            del df
        else:
            print '...aleady exists: ',saveFile
