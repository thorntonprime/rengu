# -*- coding: utf-8 -*-

import xapian
from prajna.rengu.tools import flatten

def _get_xapian_db(path, writeable=False):
    from urllib.parse import urlsplit
    from urllib.error import URLError

    url = urlsplit(path)

    if url.scheme == 'file':
        if writeable:
            return xapian.WritableDatabase(url.path, xapian.DB_CREATE_OR_OPEN)
        else:
            return xapian.Database(url.path)

    elif url.scheme == 'tcp':
        if writeable:
            return xapian.remote_open_writable(url.hostname, url.port)
        else:
            return xapian.remote_open(url.hostname, url.port)

    else:
        raise URLError(10, "Couldn't parse Xapian URL " + path)


def index(xapiandb, v):

    indexer = xapian.TermGenerator()
    stemmer = xapian.Stem("english")
    indexer.set_stemmer(stemmer)

    pk = v.pk
    title = v.get("Title")
    author = v.get("By")
    

    for line in flatten(v.get("Lines", [])):
        doc = xapian.Document()
        doc.set_data(line.strip())

        indexer.set_document(doc)
        indexer.index_text(line.lower().strip())
    
        doc.add_term("Q" + pk)
        if title:
            if len(title) > 240:
                title = title[:240]
            doc.add_term("S" + title)
        if author:
            for a in flatten([author]):
                doc.add_term("A" + a)

        if v.get("Tags"):
            for tag in flatten([t.lower().split("=") for t in v.get("Tags")]):
                doc.add_term("K" + tag)

        xapiandb.add_document(doc)

def search(xapiandb, query_string, count=1000):

    enquire = xapian.Enquire(xapiandb)

    # Parse the query string to produce a Xapian::Query object.
    qp = xapian.QueryParser()
    stemmer = xapian.Stem("english")
    qp.set_stemmer(stemmer)
    qp.set_database(xapiandb)
    qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
    query = qp.parse_query(query_string)

    if not query.empty():
        # print("Parsed query is: %s" % str(query))

        # Find the top 10 results for the query.
        enquire.set_query(query)
        matches = enquire.get_mset(0, count)

        # Display the results.
        # print("%i results found." % matches.get_matches_estimated())
        # print("Results 1-%i:" % matches.size())

        for m in matches:
            pk = None
            for term in m.document.termlist():
                k = term.term.decode("utf-8")[0]
                if k == 'Q':
                    pk = term.term.decode("utf-8")[1:]

            yield m.rank + 1, m.percent, pk, m.document.get_data().decode("utf-8")

