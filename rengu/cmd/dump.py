
import cmd

from rengu.cmd import auto_help
from rengu.config import DB


class RenguDumpCmd(cmd.Cmd):

    prompt = "dump >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_verse(self, args):
        from rengu.verse import Verse

        for pk in args.split():
            v = DB.get(Verse, {"pk": pk})
            print(v.to_yaml())

    @auto_help
    def do_source(self, args):
        from rengu.source import Source

        for pk in args.split():
            s = DB.get(Source, {"pk": pk})
            print(s.to_yaml())

    @auto_help
    def do_author(self, args):
        from rengu.author import Author

        for pk in args.split():
            a = DB.get(Author, {"pk": pk})
            print(a.to_yaml())

