
from goodreads import GoodReads
from  sys import argv


if len(argv)<3:
    print('provide author quotes url and output file name..')        
else:
    url = argv[1]
    directory = argv[2]
    print(url,directory)
    r = GoodReads(url, directory)
    if(r.countPages() > 0):
        r.getAllQuotes()
