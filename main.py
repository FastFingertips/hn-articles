import time as t
from SwSpotify import spotify
import pyautogui as pg
import json
import requests
import webbrowser


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

def main():
    articleIds = getArticles()
    print(len(articleIds))
    no = 1
    for articleId in articleIds:
        article = getArticle(articleId)
        author = article['by']
        try: comments = article['descendants']
        except KeyError: comments = 0
        id = article['id']
        try: kids = article['kids']
        except KeyError: kids = []
        score = article['score']
        time = article['time']
        title = article['title']
        type = article['type']
        try: 
            url = article['url'] 
        except KeyError: url = ''
        articleDict = {'id': id,
                       'author': author,
                       'comments': comments,
                       'kids': kids,
                       'score': score,
                       'time': time,
                       'title': title,
                       'type': type,
                       'url': url}
        print(f'{no}: {type}')
        # printing all the article info
        maxLenghtKey = max(len(key) for key in articleDict)
        for key, value in articleDict.items():
                print(f'{key}:{" "*(maxLenghtKey-len(key))} {value}')
        if url != '':
            with open('urls.txt', "r+") as f:
                urls = f.readlines()
                if  url+'\n' not in urls:
                    with open('urls.txt', "a+") as f:
                        f.write(f"{url}\n")
                    webbrowser.open(url, new=0, autoraise=True)
                    t.sleep(20)
                else:
                    print("Already read")
        no += 1
        print('\n')

if __name__ == "__main__":
    main()
    import webbrowser

url = 'https://pythonexamples.org'
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
webbrowser.get('chrome').open(url)