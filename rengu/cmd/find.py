
import cmd

import rengu.config
from rengu.cmd import auto_help

from rengu.config import DB

import json

class RenguFindCmd(cmd.Cmd):

    prompt = "find >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_verse(self, args):
        print("find verses")

    @auto_help
    def do_source(self, args):
        from rengu.source import Source

        try:
            results = [dict(x) for x in list(DB.filter(Source, eval(args)))]
            print(json.dumps(results, sort_keys=True, indent=2))
        except SyntaxError as e:
            print(e)

    @auto_help
    def do_author(self, args):
        from rengu.author import Author

        try:
            results = [dict(x) for x in list(DB.filter(Author, eval(args)))]
            print(json.dumps(results, sort_keys=True, indent=2))
        except SyntaxError as e:
            print(e)

