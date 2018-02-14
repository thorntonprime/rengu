# -*- coding: utf-8 -*-


import re
from pathlib import Path

from rengu.tags import TreasuryTagMap

from textblob import TextBlob

import yaml


Verses = []


def load():
    verses = Path('verses')

    for vfile in verses.iterdir():
        for i in yaml.load_all(open(vfile).read()):
            if i:
                i['_uid'] = vfile.name
                Verses.append(i)


def load_yaml_file(f):

    rin = open(f, 'r')
    i = f.split('/')[-1]

    rdoc = {
        "pk": i
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
                # rdoc["Lines"].append( [ {"Format" : "verse"}, ] +  lines  )
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

    # W.Perry tags by number
    if 'Tags' in rdoc:
        if isinstance(rdoc['Tags'], type(str(""))):
            tags = rdoc['Tags'].split()
            rdoc['Tags'] = tags
        else:
            for t in rdoc['Tags'].copy():
                if str(t) in TreasuryTagMap:
                    rdoc['Tags'].remove(t)
                    rdoc['Tags'].append(TreasuryTagMap[str(t)])

    # Clean up tags
    if rdoc.get("By") and isinstance(
            rdoc["By"], str) and rdoc["By"][0] == '\\':
        rdoc["By"] = rdoc["By"][1:]

    return rdoc
