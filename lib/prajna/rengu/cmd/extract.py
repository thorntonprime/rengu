
import cmd

from prajna.rengu.cmd import auto_help
from prajna.rengu.verse import Verse


class RenguExtractCmd(cmd.Cmd):

    prompt = "extract >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_words(self, args):
        '''words
        Extract all words infromation from the Verse uids.
        '''

        for verse_pk in args.split():
            v = Verse.fetch(verse_pk)
            for w in v.extract_words():
                print("{0} {1}".format(verse_pk, w.lower()))

    @auto_help
    def do_author(self, args):
        '''author
        Extract all author infromation from the Verse uids.
        '''

        for verse_pk in args.split():
            v = Verse.fetch(verse_pk)

            for role, a in v.extract_authors():
                print("{0} {1:12} {2:36} {3}".format(
                    verse_pk, role, a['pk'], a['Name']))

    def do_source(self, args):
        '''source
        Extract all source information from the Verse ids.
        '''

        for verse_pk in args.split():
            v = Verse.fetch(verse_pk)

            for s in v.extract_sources():
                print("{0} {1:36} {2} / {3}".format(verse_pk,
                                                    s['pk'], s['Title'], s.get("By", "NONE")))
