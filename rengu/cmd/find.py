
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
        print("find sources")

    @auto_help
    def do_author(self, args):
        from rengu.author import Author

        results = [dict(x) for x in list(DB.filter(Author, eval(args)))]
        print(json.dumps(results, sort_keys=True, indent=2))

