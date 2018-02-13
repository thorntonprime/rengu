# -*- coding: utf-8 -*-

from pathlib import Path

from rengu.tools import flatten, is_uuid, remove_accents

from blitzdb import Document, FileBackend

import yaml


class Author(Document):

    class Meta(Document.Meta):
        collection = 'authors'

    @staticmethod
    def read_yaml_file(fn):
        for data in yaml.load_all(open(fn).read()):
            if data:
                if not data.get('pk'):
                    from os.path import basename
                    data['pk'] = basename(fn)
                
                yield Author(data)


##### OLD STUFF BELOW HERE

Authors = []

def load():
    authors = Path('authors')

    for pfile in authors.iterdir():
        for i in yaml.load_all(open(pfile).read()):
            if i:
                i['pk'] = pfile.name
                Authors.append(i)


def find(name):
    fixed = remove_accents(name)
    for p in Authors:
        if fixed in p["Name"]:
            print(p["_uid"])


def load_authors_map():

    authors = {}
    map_file = open('docs/authors.md', 'r')

    for author in map_file.readlines():
        try:
            (wiki, data, name) = [x.strip() for x in author.split('|')]

            if is_uuid(name):
                continue

            real_name = wiki.split('](')[0][1:]
            if real_name == 'None' or real_name == '':
                real_name = name

            wiki_url = wiki.split('](')[1][:-1]
            if wiki_url == '':
                wiki_url = None

        except:
            continue

        if real_name in authors:
            authors[real_name]['AlternateNames'].append(name)
            authors[name] = {'RealName': real_name}
        else:
            if real_name == name:
                authors[real_name] = {'AlternateNames': [], 'URLs': [wiki_url] }
            else:
                authors[real_name] = {'AlternateNames': [name], 'URLs': [wiki_url]}
                authors[name] = {'RealName': real_name}

    return authors


def load_yaml_file(f):

    authors_map = load_authors_map()

    for x in yaml.load_all(open(f).read()):
        if x:

            name = x['Name']

            if name in authors_map:

                if 'RealName' in authors_map[name]:
                    x['AlternateNames'] = x.get('AlternateNames', [])
                    x['AlternateNames'].append([name])
                    name = authors_map[name]['RealName']
                    x['Name'] = name

                alternate_names = authors_map[name].get('AlternateNames', [])
                alternate_names.extend(x.get('AlternateNames', []))

                alternate_names = list(
                    set([i for i in flatten(alternate_names)]))

                if len(alternate_names) > 0:
                    x['AlternateNames'] = alternate_names

                if 'URLs' in authors_map[name]:
                    x['URLs'] = authors_map[name]['URLs']

            return x
