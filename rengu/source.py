# -*- coding: utf-8 -*-

from blitzdb import Document


class Source(Document):

    class Meta(Document.Meta):
        collection = 'sources'

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
    def read_yaml_file(fn):
        import yaml

        for data in yaml.load_all(open(fn).read()):
            if data:
                if not data.get('pk'):
                    from os.path import basename
                    data['pk'] = basename(fn)

                yield Source(data)
