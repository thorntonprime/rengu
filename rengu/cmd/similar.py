
import cmd

from rengu.cmd import auto_help
import spacy
import sys


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
            pk1 pk2 overall_similar count(lines) max(line_sim) min(line_sim) mean(line_sim) median(line_sim) stdev(line_sim)
        '''
        from rengu.verse import Verse

        nlp = spacy.load('en')

        verses = args.split()
        pka = verses[0]
        for pkb in verses[1:]:
            try:
                a = Verse.fetch(pka)
                print( pka, pkb, 
                   "{0:.4f} {1: 6g} {2:.4f} {3:.4f} {4:.4f} {5:.4f} {6:.4f}".format( *a.similar(pkb, nlp=nlp))  )
                sys.stdout.flush()
            except Exception as e:
                print(pka, pkb, "ERROR", e)

    def do_lines(self, args):
        '''verse pk1 pk2
        Will compute similarity of the lines of tweo verses
        Output is:
            pk1 pk2 similarity line1 line2
        '''
        from rengu.verse import Verse

        try:
            pka, pkb = args.split()
        except ValueError:
            print("ERROR wrong number of verses to compare")
            return False

        nlp = spacy.load('en')

        a = Verse.fetch(pka)
        b = Verse.fetch(pkb)

        for s in a.similar_lines(b):
            print(s)


