
import sys
sys.path.append('')

from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
import pickle

CL_PICKLE_FILE = "output/tag-classifier.pickle"


def load_classifier():

    try:
        fin = open(CL_PICKLE_FILE, 'rb')
        return pickle.load(fin)

    except FileNotFoundError:
        return NaiveBayesClassifier([])


def dump_classifier(cl):
    fout = open(CL_PICKLE_FILE, 'wb')
    pickle.dump(cl, fout)


def _get_tags(v):

    for tag in v.get('Tags', []):
        for tag_x in [x for x in tag.split("=") if len(x) > 0]:
            yield tag_x


def train(cl, v):

    tag_list = set(_get_tags(v))

    for tag in tag_list:
        cl.update([(v.Body, tag)])

    return list(tag_list)


def show(cl, v):

    tag_list = cl.labels()

    for tag in tag_list:
        p = cl.prob_classify(v.Body)
        yield tag, p.prob(tag)
