# -*- coding: utf-8 -*-

from blitzdb import Document

class Verse(Document):

    def to_yaml(self):
        import yaml
        from prajna.rengu.tools import YamlDumper

        v = dict(self)
        body = v["Body"].replace(":", "：")
        if body[0] in [" ", "'", '"', ".", "["]:
            body = "\\" + body

        del v["Body"]
        if v.get("Lines"):
            del v["Lines"]

        return "---\n" + yaml.dump(v, Dumper=YamlDumper,
                                   default_flow_style=False, width=70, allow_unicode=True,
                                   indent=2).strip() + "\n---\n" + body

    def to_json(self):
        import json
        return json.dumps(dict(self), sort_keys=True, indent=2)

    @staticmethod
    def fetch(pk):
        return DB.get(Verse, {"pk": pk})

    @staticmethod
    def search(query):
        return DB.filter(Verse, eval(query))

    @staticmethod
    def find(query, field="Title"):

        for a in DB.filter(Verse, {field: query}):
            yield a

