import requests
import os

class ReadSrc:

    directory = ''
    url = ''
    pages = []

    def __init__(self, directory, url, pages):
        self.directory = directory
        self.url = url
        self.pages = pages

    def get(self, url):
        while(True):
            request = requests.get(url)
            if(request.status_code == 200):
                return request.content

    def getText(self, url):
        while(True):
            request = requests.get(url)
            if(request.status_code == 200):
                request.encoding='utf-8'
                return request.text

    def getAll(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        for i in range(self.pages[0], self.pages[1]+1, 1):
            save_url = "%s/page%s.txt" % (self.directory, i)
            page_url = self.url+str(i)
            print(page_url)
            f = open(save_url, "wb")
            src = self.get(page_url)
            f.write(src)
            f.close()
