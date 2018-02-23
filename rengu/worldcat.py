

import string
import urllib.parse

from bs4 import BeautifulSoup

from rengu.config import WORLDCAT_BASEURL, worldcat_PASSWORD, worldcat_USERNAME

import requests


worldcat = requests.Session()
response = worldcat.post(WORLDCAT_BASEURL + "/account/",
                         data={"username": worldcat_USERNAME,
                               "password": worldcat_PASSWORD})


def search_title(title):
    return search_book(urllib.parse.quote("t:" + title))


def search_isbn(isbn):
    return search_book(urllib.parse.quote("bn:" + str(isbn)))


def search_book(query):
    url = WORLDCAT_BASEURL + "/search?q=" + query

    response = worldcat.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    books = soup.find_all('td', class_='result details')

    if len(books) > 0:

        url = WORLDCAT_BASEURL + books[0].a['href']

        response = worldcat.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1', class_='title')
        author = soup.find('td', {"id": 'bib-author-cell'})
        publisher = soup.find('td', {"id": 'bib-publisher-cell'})

        print(url)
        print(string.capwords(title.text))

        if author:
            print(author.text)
        else:
            print("NO AUTHOR")

        if publisher:
            print(publisher.text)

        authors = soup.find('tr', {"id": "details-allauthors"})
        if authors:
            for a in authors.find_all('a'):
                print(a.text)

        isbn = soup.find('tr', {"id": "details-standardno"})
        if isbn:
            print(isbn.td.text)

        oclc = soup.find('tr', {"id": "details-oclcno"})
        if oclc:
            print(oclc.td.text)

        print()

    else:
        print("Not found")

    print()
