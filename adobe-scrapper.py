import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import csv

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

pageUrl = list()
data = dict()

url = 'https://stock.adobe.com/search/images?filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Aillustration%5D=1&filters%5Bcontent_type%3Azip_vector%5D=1&filters%5Bcontent_type%3Avideo%5D=0&filters%5Bcontent_type%3Atemplate%5D=0&filters%5Bcontent_type%3A3d%5D=0&filters%5Binclude_stock_enterprise%5D=0&filters%5Bis_editorial%5D=0&filters%5Bcontent_type%3Aimage%5D=1&k=travel+couple&order=relevance&price%5B%24%5D=1&safe_search=1&search_page=38&get_facets=0&search_type=pagination'

html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html,'html.parser')
tags = soup('a')

for link in tags:
    href = link.get('href',None)
    if href is None:
        continue
    if href.startswith('https://stock.adobe.com/in/images/'):
        pageUrl.append(href)

with open('adobe.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    for url in pageUrl:
        try:
            html = urllib.request.urlopen(url, context=ctx).read()
        except:
            continue
        soup = BeautifulSoup(html,'html.parser')
        divs = soup('div')
        titles = soup('title')

        for title in titles:
            scrappedCaption = title.contents[0]
            caption = scrappedCaption[:-78]

        for div in divs:
            divData = div.get('id',None)
            if divData is None or divData != 'image-detail-json':
                continue
            content = div.contents[0]
            startPos = content.find('author')
            endPos = content.find('author_url')
            author = content[startPos+9:endPos-3]

        writer.writerow([url,caption,author])
