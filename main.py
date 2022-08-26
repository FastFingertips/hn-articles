import os
import json
import requests
import webbrowser
import time as time
from datetime import datetime

def getTimestamp():
    dt = datetime.now()
    return int(datetime.timestamp(dt)) # r:int

def timestampToDate(ts):
    dateFormat = '%Y.%m.%d %H:%M:%S'
    dt = datetime.fromtimestamp(ts)
    return dt.strftime(dateFormat) # r:str

def dateToTimestamp(dt):
    dateFormat = '%Y.%m.%d %H:%M:%S'
    sdt = datetime.strptime(dt, dateFormat)
    return int(datetime.timestamp(sdt)) # r:int

def readtxtfilelines():
    with open("urls.txt", 'r') as f:
        return f.readlines()

def urlcheck(url):
    filename = "urls.json"
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({}, f)
            print("File created")
            time.sleep(4)

    jsonFile = open(filename, "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file

    print('Visit: ', end='')
    if url in data.keys(): 
        print(timestampToDate(int(data[url])))
        return False
    else:
        data[url] = str(getTimestamp())
        jsonFile = open(filename, "w+") # Save our changes to JSON file
        jsonFile.write(json.dumps(data, indent=4))
        jsonFile.close()
        print(timestampToDate(getTimestamp()), 'New Visit!')
        return True

def getArticles():
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    r = requests.get(url)
    return r.json()

def getArticle(id):
    url = 'https://hacker-news.firebaseio.com/v0/item/' + str(id) + '.json'
    r = requests.get(url)
    return r.json()

def articleParser(article_json):
    d = {
         'gets': {
          'id': None,
          'by': None,
          'descendants': 0, # sometimes article has no comments
          'kids': [],
          'score': None,
          'time': None,
          'title': None,
          'type': None,
          'url': ''
          },
          'rets': {
          }
         }

    for getKey, exceptValue in d['gets'].items():
        try: d['rets'][getKey] = article_json[getKey]
        except KeyError: 
            if exceptValue != None: d['rets'][getKey] = exceptValue
            else: print(f'{getKey} not found')
    print(json.dumps(d, indent=1))
    return d['rets']


def dictToTable(dict, table_name):
    from rich.console import Console
    from rich.table import Table
    console = Console()
    t = Table(title=table_name)
    for col in dict.keys(): t.add_column(col)
    rows = []
    for row in dict.values(): 
        try: rows.append(str(row))
        except: rows.append(row)
    t.add_row(*rows)
    console.print(t)

def parallelBlank(str, dict):
    maxLenghtKey = max(len(key) for key in dict)
    parallelBlank = ' ' * (maxLenghtKey - len(str))
    return parallelBlank

def main():
    articleIds = getArticles()
    for rank, articleId in enumerate(articleIds):
        articleJson = getArticle(articleId)
        articleDict = articleParser(articleJson)

        # dictToTable(articleDict, articleDict["title"])
        no = str(rank + 1)
        print(no)
        for key, value in articleDict.items():
            blanks = parallelBlank(key, articleDict)
            print(f'{key}:{blanks} {value}')

        url = articleDict['url']
        if url != '':
            filechange = urlcheck(url)
            if filechange:
                webbrowser.open(url, new=2)
                time.sleep(60)

        print('\n')

if __name__ == "__main__":
    main()