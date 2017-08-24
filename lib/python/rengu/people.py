# -*- coding: utf-8 -*-

from pathlib import Path
import yaml

from rengu.tools import *

People = []

def load():
    people = Path('people')
    
    for pfile in people.iterdir():
        for i in yaml.load_all(open(pfile).read()):
            if i:
                i['_uid'] = pfile.name
                People.append(i)

def find(name):
    fixed = remove_accents(name)
    for p in People:
        if fixed in p["Name"]:
            print(p["_uid"])
