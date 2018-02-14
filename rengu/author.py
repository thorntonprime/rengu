# -*- coding: utf-8 -*-

from blitzdb import Document
from rengu.config import DB


class Author(Document):

    def to_yaml(self):
        import yaml
        from rengu.tools import YamlDumper

        return "---\n" + yaml.dump(dict(self),
                                   Dumper=YamlDumper, default_flow_style=False,
                                   width=70, indent=2).strip() + "\n---"

    def to_json(self):
        import json
        return json.dumps(dict(self), sort_keys=True, indent=2)


    @staticmethod
    def fetch(pk):
        return DB.get(Author, {"pk": pk})

    @staticmethod
    def search(query):
        return DB.filter(Author, eval(query))

    @staticmethod
    def find(query, field="Name"):

        found = set()

        for a in DB.filter(Author, { field: query } ):
            if a.pk not in found:
                found.add(a.pk)
                yield a

        if field == "Name":
            for a in DB.filter(Author, { "AlternateNames": query } ):
                if a.pk not in found:
                    found.add(a.pk)
                    yield a


    @staticmethod
    def read_yaml_file(fn):
        import yaml

        for data in yaml.load_all(open(fn).read()):
            if data:
                if not data.get('pk'):
                    from os.path import basename
                    data['pk'] = basename(fn)

                yield Author(data)


    # Class internal data and methods ###############################
    class Meta(Document.Meta):
        primary_key = 'pk'
        collection = 'authors'

from pymongo import ASCENDING
DB.create_index(Author, 'Name', fields={"Name": ASCENDING}, unique=True, ephemeral=False )
DB.create_index(Author, 'AlternateNames', fields={"AlternateNames": ASCENDING}, unique=True, ephemeral=False )

