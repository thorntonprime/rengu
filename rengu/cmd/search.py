
import cmd

from rengu.cmd import auto_help
from rengu.config import DB


class RenguSearchCmd(cmd.Cmd):

    prompt = "search >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_verse(self, args):
        from rengu.verse import Verse

        try:
            for v in DB.filter(Verse, eval(args)):
                print(v.to_json())
        except SyntaxError as e:
            print(e)

    @auto_help
    def do_source(self, args):
        from rengu.source import Source

        try:
            for s in DB.filter(Source, eval(args)):
                print(s.to_json())
        except SyntaxError as e:
            print(e)

    @auto_help
    def do_author(self, args):
        from rengu.author import Author

        try:
            for a in DB.filter(Author, eval(args)):
                print(a.to_json())

        except SyntaxError as e:
            print(e)