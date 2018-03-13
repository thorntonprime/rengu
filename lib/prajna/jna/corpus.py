
from gensim import corpora
from prajna.jna.verse import Verse


# from nltk.corpus import stopwords
# stopWords = set(stopwords.words('english'))

def build_dictionary() {
    pass


class JnaCorpus(object):

    def __init__(self, *verses):
        super(JnaCorpus, self).__init__()
        self.verses = verses[0]

    def __iter__(self):
        dictionary = corpora.Dictionary()

        for pk in self.verses:
            v = Verse.fetch(pk)
            for block in v.get("Lines", []):
                for line in block:
                    print (dictionary.doc2bow(line.lower().split()))
                    yield dictionary.doc2bow(line.lower().split())
