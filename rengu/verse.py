# -*- coding: utf-8 -*-

import re
from pathlib import Path

from blitzdb import Document


from textblob import TextBlob


class Verse(Document):

    class Meta(Document.Meta):
        collection = 'verses'

    def to_yaml(self):
        import yaml
        from rengu.tools import YamlDumper

        v = dict(self)
        body = v["Body"].replace(":", "：")
        if body[0] == "'" or body[0] == '"' or body[0:3] == "...":
            body = "\\" + body

        del v["Body"]
        del v["Lines"]

        return "---\n" + yaml.dump(v, Dumper=YamlDumper,
                                   default_flow_style=False, width=70, indent=2).strip() + \
            "\n---\n" + body

    def to_json(self):
        import json
        return json.dumps(dict(self), sort_keys=True, indent=2)

    @staticmethod
    def read_yaml_file(fn):
        from os.path import basename
        import yaml

        rin = open(fn, 'r')

        rdoc = {
            'pk': basename(fn)
        }

        # Read in the default document to handle as the Body
        doc = ""
        for l in rin.readlines():

            # some text clean-up
            l = re.sub("[`‘’`’‘’]", "'", l)
            l = re.sub('[”"“]', '"', l)
            # l = re.sub(r": \\\'", ": '", l)

            if l.strip() == '---':
                y = yaml.load(doc)

                if isinstance(y, dict):
                    rdoc = {**rdoc, **y}

                if isinstance(y, str):
                    rdoc['Body'] = doc

                doc = ""
                next
            else:
                doc += l

        # convert hack text
        doc = re.sub("：", ":", doc)
        doc = re.sub("\\\\", "", doc)

        # set up array for lines
        rdoc["Lines"] = []

        # prose is split into paragraphs and split into sentances
        if not ('Format' in rdoc) or (rdoc['Format'].lower() == 'prose'):
            for p in re.split("\n\n", doc):

                    # Scrub extraneous newlines and spaces
                p = re.sub("(?<!\n)\n(?!\n)", " ", p)
                p = re.sub(" +", " ", p)

                blob = TextBlob(p)

                lines = [str(x.strip()) for x in blob.sentences]
                rdoc["Lines"].append(lines)

        # verse should be read line by line
        elif rdoc['Format'].lower() == 'verse':
            for p in re.split("\n\n", doc):
                lines = [re.sub("\n", "", x.rstrip())
                         for x in re.split("\n(?! \w)", p.rstrip())]

                rdoc["Lines"].append(lines)

        # Structured format ... TBD
        elif rdoc['Format'].lower() == 'structured':
            del(rdoc['Lines'])
            rdoc['Structure'] = yaml.load(doc)

        # else mixed format
        else:
            for p in re.split("\n\n", doc):

                # verse lines start with one or more spaces
                if re.match("^ +", p):
                    lines = [re.sub("\n", " ", x).rstrip()
                             for x in re.split("\n(?=\s+)", p.rstrip())]
                    rdoc["Lines"].append(lines)

                else:
                    # Scrub extraneous newlines and spaces
                    p = re.sub("(?<!\n)\n(?!\n)", " ", p)
                    p = re.sub(" +", " ", p)

                    blob = TextBlob(p)

                    lines = [str(x.strip()) for x in blob.sentences]
                    rdoc["Lines"].append(lines)

        # Set Body, remove final CR
        rdoc['Body'] = doc.rstrip()

        # Unescape By Field
        if rdoc.get("By") and isinstance(
                rdoc["By"], str) and rdoc["By"][0] == '\\':
            rdoc["By"] = rdoc["By"][1:]

        return Verse(rdoc)
