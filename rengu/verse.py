# -*- coding: utf-8 -*-

import re

from blitzdb import Document

from rengu.config import DB

from textblob import TextBlob


class Verse(Document):

    def similar_lines(self, other, nlp=None):
        import spacy
        import itertools
        from statistics import mean, median, stdev

        if nlp == None:
            nlp = spacy.load('en')

        for self_line in list(itertools.chain(*self.get("Lines", []))):
            self_line_doc = nlp(self_line)
            if len(self_line_doc) < 2:
                continue

            for other_line in list(itertools.chain(*other.get("Lines", []))):
                other_line_doc = nlp(other_line)
                if len(other_line_doc) < 2:
                    continue

                similar = self_line_doc.similarity(other_line_doc)
                yield similar, self_line, other_line

    def similar(self, other_pk, nlp=None):
        import spacy
        import itertools
        from statistics import mean, median, stdev

        if nlp == None:
            nlp = spacy.load('en')

        other = Verse.fetch(other_pk)

        self_doc = nlp(self["Body"])
        other_doc = nlp(other["Body"])

        similar = self_doc.similarity(other_doc)

        line_sim = [x[0] for x in self.similar_lines(other, nlp)]

        line_len = len(line_sim)

        if line_len > 0:
            line_max = max(line_sim)
            line_min = min(line_sim)
            line_mean = mean(line_sim)
            line_median = median(line_sim)
        else:
            line_max = 0
            line_min = 0
            line_mean = 0
            line_median = 0

        if line_len > 1:
            line_stdev = stdev(line_sim)
        else:
            line_stdev = 0

        return similar, line_len, line_max, line_min, line_mean, line_median, line_stdev

    def to_yaml(self):
        import yaml
        from rengu.tools import YamlDumper

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

        if rdoc.get("Title") and rdoc["Title"][0] == '\\':
            rdoc["Title"] = rdoc["Title"][1:]

        return Verse(rdoc)

    class Meta(Document.Meta):
        primary_key = 'pk'
        collection = 'verses'


#####################################################################
# Create indexes

from blitzdb.queryset import QuerySet
DB.create_index(Verse, 'Title', fields={
                "Title": QuerySet.ASCENDING}, unique=False, ephemeral=False)
DB.create_index(Verse, 'Tags', fields={
                "Tags": QuerySet.ASCENDING}, unique=False, ephemeral=False)
