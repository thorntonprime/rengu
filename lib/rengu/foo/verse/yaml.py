
from . import Verse
import re

from textblob import TextBlob
from os.path import basename
import yaml

def read_yaml_file(fn):

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


