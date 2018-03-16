# -*- coding: utf-8 -*-

import xapian


def index(v):

    database = xapian.WritableDatabase(sys.argv[1], xapian.DB_CREATE_OR_OPEN)

    indexer = xapian.TermGenerator()
    stemmer = xapian.Stem("english")
    indexer.set_stemmer(stemmer)
