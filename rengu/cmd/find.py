
import cmd
import json

from rengu.cmd import auto_help
from rengu.config import DB


class RenguFindCmd(cmd.Cmd):

    prompt = "find >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_verse(self, args):
        from rengu.verse import Verse

        try:
            for v in DB.filter(Verse, eval(args)):
                print(json.dumps(dict(v), sort_keys=True, indent=2))
        except SyntaxError as e:
            print(e)

    @auto_help
    def do_source(self, args):
        from rengu.source import Source

        try:
            for s in DB.filter(Source, eval(args)):
                print(json.dumps(dict(s), sort_keys=True, indent=2))
        except SyntaxError as e:
            print(e)

    @auto_help
    def do_author(self, args):
        from rengu.author import Author

        try:
            for a in DB.filter(Author, eval(args)):
                print(json.dumps(dict(a), sort_keys=True, indent=2))

        except SyntaxError as e:
            print(e)
