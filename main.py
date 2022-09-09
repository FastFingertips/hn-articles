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

def countdown(t, msg='{}'):
 while t:
    mins, secs = divmod(t, 60)
    timer = '{:02d}:{:02d}'.format(mins, secs)
    os.system(f'title {msg}'.format(timer)) 
    time.sleep(1)
    t -= 1

def urlcheck(url):
    filename = "urls.json"
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({}, f)
            print("File created")
            countdown(4, 'Continue in: {}')

    jsonFile = open(filename, "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file

    print('Visit: ', end='')
    if url in data.keys(): 
        print(timestampToDate(int(data[url])))
        print(f'Url No: {list(data.keys()).index(url) + 1}')
        return False
    else:
        data[url] = str(getTimestamp())
        jsonFile = open(filename, "w+") # Save our changes to JSON file
        jsonFile.write(json.dumps(data, indent=4))
        jsonFile.close()

        print(timestampToDate(getTimestamp()), 'New Visit!')
        print(f'Url Count: {len(data.keys())}')
        return True

def getReq(url, timeout=5):
    while True:
        try: return requests.get(url, timeout=timeout)
        except requests.ConnectionError: # check internet connection
            print("No internet connection available.", end='\r')
            time.sleep(1)

def getArticles():
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    r = getReq(url)
    return r.json()

def getArticle(id):
    url = 'https://hacker-news.firebaseio.com/v0/item/' + str(id) + '.json'
    r = getReq(url)
    return r.json()

def articleParser(article_json):
    data = {'id': None,
           'by': None,
           'descendants': 0, # sometimes article has no comments
           'kids': [],
           'score': None,
           'time': None,
           'title': None,
           'type': None,
           'url': ''}

    for getKey, exceptValue in data.items():
        try: data[getKey] = article_json[getKey]
        except KeyError: 
            if exceptValue != None: data[getKey] = exceptValue
            else: print(f'{getKey} not found')
    return data

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

def cryptoEffect(v):
    import random
    print(v,end="")
    print("\r", end="") 
    words = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    numbers = random.sample(range(1, 100), 10)

    numbers = [str(i) for i in numbers] 
    for n in numbers:
        randomNumbers = (random.choice(numbers) * random.randint(0, len(v)))[:len(v)]
        randomWords = ''.join(random.choice(words) for i in range(len(v)))
        print(randomNumbers,  end="\r")
        print(randomWords, end="\r")
        randomSleep = random.randint(0, 100) / 300
        time.sleep(randomSleep)


def defaultReworker(defaultValue, minValue, maxValue, q):
    cryptoEffect(q)
    while True:
        reValue = input(f'{q} (default: {defaultValue})\n')
        if len(reValue) == 0: 
            print(f'Using default value: {defaultValue}')
            return defaultValue

        try:
            reValue = int(reValue)
            if reValue <= maxValue and reValue > minValue: return reValue
            else: print(f'Please enter a number between {minValue} and {maxValue}, or leave blank for default', defaultValue)
        except ValueError: print('Please enter a number')

def main():
    articleCount = defaultReworker(50, 0, 500, 'How many articles do you want to see?')
    articleCountdown = defaultReworker(60, 0, 3600, 'How many seconds do you want to wait between each article?')

    while True:
        print('Getting articles...\n')
        os.system(f'title Getting articles...  ') 
        articleIds = getArticles()
        for rank, articleId in enumerate(articleIds):
            os.system(f'title Article: {articleCount}/{rank}') 
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
                    countdown(articleCountdown, 'Next article in: {}')
            print('\n')
            if rank == articleCount: print(f'Top {articleCount} articles reached!'); break

if __name__ == "__main__": main()