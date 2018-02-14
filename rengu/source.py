# -*- coding: utf-8 -*-

from pathlib import Path

from rengu.tools import remove_accents

from blitzdb import Document, FileBackend

import yaml

class Source(Document):

    class Meta(Document.Meta):
        collection = 'sources'

    @staticmethod
    def read_yaml_file(fn):
        for data in yaml.load_all(open(fn).read()):
            if data:
                if not data.get('pk'):
                    from os.path import basename
                    data['pk'] = basename(fn)
                
                yield Source(data)

############

Sources = []


def load():
    sources = Path('sources')

    for sfile in sources.iterdir():
        for i in yaml.load_all(open(sfile).read()):
            if i:
                i['_uid'] = sfile.name
                Sources.append(i)


def find(name):
    fixed = remove_accents(name)
    for p in Sources:
        if fixed in p["Title"]:
            print(p["_uid"])


def load_yaml_file(f):

    for x in yaml.load_all(open(f).read()):
        if x:
            return x
