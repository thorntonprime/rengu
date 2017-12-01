# -*- coding: utf-8 -*-

from pathlib import Path
import yaml

from rengu.tools import *

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
