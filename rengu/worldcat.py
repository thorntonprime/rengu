

import string
import urllib.parse

from bs4 import BeautifulSoup

from rengu.config import WORLDCAT_BASEURL, worldcat_PASSWORD, worldcat_USERNAME
from rengu.tools import is_isbn

import requests


worldcat = requests.Session()
response = worldcat.post(WORLDCAT_BASEURL + "/account/",
                         data={"username": worldcat_USERNAME,
                               "password": worldcat_PASSWORD})


def search_title_author(title, author):
    return search_book(urllib.parse.quote("ti:" + title))


def search_title(title):
    return search_book(urllib.parse.quote("ti:" + title))


def search_isbn(isbn):
    return search_book(urllib.parse.quote("bn:" + str(isbn)))


def search_book(query):
    url = WORLDCAT_BASEURL + "/search?q=" + query

    response = worldcat.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    books = soup.find_all('td', class_='result details')

    if len(books) > 0:

        url = WORLDCAT_BASEURL + books[0].a['href']

        data = {}

        response = worldcat.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        title_soup = soup.find('h1', class_='title')
        publisher = soup.find('td', {"id": 'bib-publisher-cell'})

        titles = [t.strip() for t in title_soup.text.split(':')]

        data['Title'] = string.capwords(titles[0]).strip()

        if len(titles) > 1:
            data["Subtitle"] = string.capwords(titles[1]).strip()

        if len(titles) > 2:
            data["AlternateTitles"] = [
                string.capwords(t).strip() for t in titles[2:]]

        authors = soup.find('tr', {"id": "details-allauthors"})
        if authors:
            data["By"] = []
            for a in authors.find_all('a'):
                data["By"].append(a.text.strip())

        isbn = soup.find('tr', {"id": "details-standardno"})
        if isbn and isbn.text:
            data["Publications"] = [{"ISBN": isbn.text.split()[1:]}]

        if publisher:
            if data.get("Publications"):
                data["Publications"][0][
                    "Publisher"] = publisher.text.replace(':', ';')
            else:
                data["Publications"] = [
                    {"Publisher": publisher.text.replace(':', ';')}]

        oclc = soup.find('tr', {"id": "details-oclcno"})
        if oclc:
            data["Worldcat"] = {"OCLC": oclc.td.text}

        return data

    else:
        return None
