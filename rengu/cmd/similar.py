
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
        from rengu.verse import Verse

        for pka in args.split():
            for pkb in [ x for x in args.split() if x != pka ]:
                a = Verse.fetch(pka)
                print(pka, pkb, a.similar(pkb))

