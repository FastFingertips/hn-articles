import time
from SwSpotify import spotify
import pyautogui as pg
import json
import requests

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
    print(articleIds)
    for articleId in articleIds:
        article = getArticle(articleId)
        title = article['title']
        author = article['by']
        try:
            comments = article['descendants']
        except KeyError:
            comments = 0
        id = article['id']
        try:
            kids = article['kids']
        except KeyError:
            kids = []
        score = article['score']
        time = article['time']
        type = article['type']
        try:
            url = article['url'] 
        except KeyError:
            url = 'No URL'
        articleDict = {'id': id,
                       'author': author,
                       'comments': comments,
                       'kids': kids,
                       'score': score,
                       'time': time,
                       'title': title,
                       'type': type,
                       'url': url}
        # printing all the article info
        maxLenghtKey = max(len(key) for key in articleDict)
        for key, value in articleDict.items():
            print(f'{key}:{" "*(maxLenghtKey-len(key))} {value}')
        print('\n')
        

if __name__ == "__main__":
    main()