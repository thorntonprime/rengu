# -*- coding: utf-8 -*-

from blitzdb import Document
from rengu.config import DB



class Source(Document):

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
        return DB.get(Source, {"pk": pk})

    @staticmethod
    def search(query):
        return DB.filter(Source, eval(query))
 
    @staticmethod
    def find(query, field="Title"):

        found = set()

        for a in DB.filter(Source, { field: query } ):
            if not a.pk in found:
                found.add(a.pk)
                yield a

        if field == "Title":
            for a in DB.filter(Source, { "AlternateTitles": query } ):
                if not a.pk in found:
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

                yield Source(data)

    class Meta(Document.Meta):
        primary_key = 'pk'
        collection = 'sources'


from pymongo import ASCENDING
DB.create_index(Source, 'Title', fields={"Title": ASCENDING}, unique=False, ephemeral=False )

