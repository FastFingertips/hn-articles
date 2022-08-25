import time as t
import requests
import webbrowser
from datetime import datetime
import json

def getTimestamp():
    dt = datetime.now()
    timestamp = int(datetime.timestamp(dt))
    return timestamp

def timestampConverter(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    sdt = dt.strftime("%Y.%m.%d, %H:%M:%S")
    return sdt

def readtxtfilelines():
    with open("urls.txt", 'r') as f:
        return f.readlines()

def urlcheck(url):
    import os
    filename = "urls.json"
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({}, f)
            print("File created")
            t.sleep(4)

    jsonFile = open(filename, "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file

    print('Visit: ', end='')
    if url in data.keys(): 
        print(timestampConverter(int(data[url])))
        return False
    else:
        data[url] = str(getTimestamp())
        jsonFile = open(filename, "w+") # Save our changes to JSON file
        jsonFile.write(json.dumps(data, indent=4))
        jsonFile.close()
        print(timestampConverter(getTimestamp()), 'New Visit!')
        return True

def getArticles():
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    r = requests.get(url)
    return r.json()

def getArticle(id):
    url = 'https://hacker-news.firebaseio.com/v0/item/' + str(id) + '.json'
    r = requests.get(url)
    return r.json()

def getArticleTitle(id):
    article = getArticle(id)
    return article['title']

def getArticleUrl(id):
    article = getArticle(id)
    return article['url']

def getArticleScore(id):
    article = getArticle(id)
    return article['score']

def getArticleTime(id):
    article = getArticle(id)
    return article['time']

def getArticleComments(id):
    article = getArticle(id)
    return article['descendants']

def getArticleAuthor(id):
    article = getArticle(id)
    return article['by']

def getArticleText(id): # returns the text of the article
    article = getArticle(id)
    return article['text']

def articleParser(article_json):
    g =     {'id':None,
            'by':None,
            'descendants': 0, # sometimes article has no comments
            'kids':[],
            'score':None,
            'time':None,
            'title':None,
            'type':None,
            'url':''}
    r =    {}
    for getKey , exceptValue in g.items():
        try: r[getKey] = article_json[getKey]
        except KeyError:
            if exceptValue != None: r[getKey] = exceptValue
            else: print(f'KeyError: {getKey}')
    return r

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

def main():
    articleIds = getArticles()
    print(len(articleIds))
    for rank, articleId in enumerate(articleIds):
        articleJson = getArticle(articleId)
        articleDict = articleParser(articleJson)

        print(f'{rank+1}: {articleDict["type"]}')
        # dictToTable(articleDict, articleDict["title"])
        for key, value in articleDict.items():
            maxLenghtKey = max(len(key) for key in articleDict)
            print(f'{key}:{" "*(maxLenghtKey-len(key))} {value}')

        url = articleDict['url']
        if url != '':
            filechange = urlcheck(url)
            if filechange:
                webbrowser.open(url, new=2)
                t.sleep(0)
        print('\n')

if __name__ == "__main__":
    main()