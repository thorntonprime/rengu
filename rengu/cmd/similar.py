
import cmd

from rengu.cmd import auto_help


class RenguSimilarCmd(cmd.Cmd):

    prompt = "similar >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_verse(self, args):
        '''verse pk1 pk2 pk3 pk4 ...
        Will compute similarity of the body of the listed verses. It compares the first
        listed verse to all the others in the list.
        
        Output is:
            pk1 pk2 overall_similar max(line_sim) min(line_sim) mean(line_sim) median(line_sim) stdev(line_sim)
        '''
        from rengu.verse import Verse
        import spacy
        import sys

        nlp = spacy.load('en')

        verses = args.split()
        pka = verses[0]
        for pkb in verses[1:]:
            try:
                a = Verse.fetch(pka)
                print(pka, pkb, ' '.join( '{0:.4f}'.format(x) for x in a.similar(pkb, nlp=nlp)) )
                sys.stdout.flush()
            except Exception as e:
                print(pka, pkb, "ERROR", e)

