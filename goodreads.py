from readsrc import ReadSrc
from bs4 import BeautifulSoup
import os
import json as json_converter


class GoodReads(ReadSrc):
    url = ''
    json = ''
    isLast = False
    allQuotes = 0

    def __init__(self, url, directory):
        self.directory = directory
        self.url = url+'?page='
        #if not os.path.exists(directory):
        #    os.makedirs(directory)
        #self.json = open("%s/quotes.json" % directory, 'w+', encoding='utf-8')
        self.json = open("outputs/%s.json" % directory, 'w+', encoding='utf-8')

    def countPages(self):
        src = self.getText(self.url+'1')
        i = src.find('</a> <a class="next_page"')
        if(i != -1):
            src = src[:i]
            j = src.rfind('>')
            if(j != -1):
                src = int(src[j+1:])
                self.pages = [1, src]
                print('range', self.pages)
                return src
        return 0

    def getQuotes(self, url):
        src = self.getText(url)
        soup = BeautifulSoup(src, features="html.parser")
        divs = soup.findAll("div", {"class": "quoteText"})
        n = len(divs)
        for index in range(n):
            div = divs[index]
            author=''
            title=''
            span = div.find({"span": "authorOrTitle"})
            a = div.find({"a": "authorOrTitle"})
            if(span):
              author=span.get_text().strip()
            if(a):  
              title=a.get_text().strip()

            text = div.get_text()
            i = text.find('“')
            j = text.find('”')

            if(i == -1 or j == -1):
                continue
            text = text[i+1:j]
            text = text.replace('\xa0','')
            quote={'author':author,'title':title,'text':text}
            
            self.json.write(json_converter.dumps(quote))
            
            if self.isLast == True and index+1 == n:
                self.json.write('\n]')
            else:
                self.json.write(',\n')
            self.allQuotes += 1


    def getAllQuotes(self):
        self.json.truncate(0)
        self.json.write('[')
        for i in range(self.pages[0], self.pages[1]+1, 1):
            if(i == self.pages[1]):
                self.isLast = True
            url = self.url+str(i)
            print(url)
            self.getQuotes(url)
        self.json.close()
        print('found', self.allQuotes)
        print('done')
