# -*- coding: utf-8 -*-

from pathlib import Path

from rengu.tools import flatten, is_uuid, remove_accents

import yaml

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


def load_people_map():

    people = {}
    map_file = open('docs/people.md', 'r')

    for person in map_file.readlines():
        try:
            (wiki, data, name) = [x.strip() for x in person.split('|')]

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

        if real_name in people:
            people[real_name]['AlternateNames'].append(name)
            people[name] = {'RealName': real_name}
        else:
            if real_name == name:
                people[real_name] = {'AlternateNames': [], 'Url': wiki_url}
            else:
                people[real_name] = {'AlternateNames': [name], 'Url': wiki_url}
                people[name] = {'RealName': real_name}

    return people


def load_yaml_file(f):

    people_map = load_people_map()

    for x in yaml.load_all(open(f).read()):
        if x:

            name = x['Name']

            if name in people_map:

                if 'RealName' in people_map[name]:
                    x['AlternateNames'] = x.get('AlternateNames', [])
                    x['AlternateNames'].append([name])
                    name = people_map[name]['RealName']
                    x['Name'] = name

                alternate_names = people_map[name].get('AlternateNames', [])
                alternate_names.extend(x.get('AlternateNames', []))

                alternate_names = list(
                    set([i for i in flatten(alternate_names)]))

                if len(alternate_names) > 0:
                    x['AlternateNames'] = alternate_names

                if 'Url' in people_map[name]:
                    x['Url'] = people_map[name]['Url']

            return x
