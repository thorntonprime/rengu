
import cmd
import os
import sys

from prajna.jna.cmd import auto_help
from prajna.jna.corpus import JnaCorpus
from gensim import corpora


class JnaCorpusCmd(cmd.Cmd):

    prompt = "corpus >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_create(self, arg):
        '''create <corpusname> verse-uuid [...]
        Create a corpus from specified verse UUIDs.
        '''

        corpus = None
        args = arg.split()

        try:
            corpus_name = args[0]

        except IndexError:
            print("Must specify corpus name.")
            sys.exit(1)

        corpus = JnaCorpus(args[1:])

        corpora.MmCorpus.serialize("corpus/" + corpus_name, corpus)
        m = corpora.MmCorpus("corpus/" + corpus_name)
        print(corpus_name, "saved", list(m.dfs))

    @auto_help
    def do_prepare(self, args):
        '''prepare
        Build dictionaries and other files used by corpus
        '''

        print("prepare")
