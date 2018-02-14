import cmd

from rengu.cmd import auto_help
import json
import sys

class RenguJSONCmd(cmd.Cmd):

    prompt = "json >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_verse(self, args):
        from rengu.verse import Verse

        for fn in args.split():
            v = dict(Verse.read_yaml_file(fn))
            print(json.dumps(v, sort_keys=True, indent=2))

    @auto_help
    def do_source(self, args):
        from rengu.source import Source

        for fn in args.split():
            for d in Source.read_yaml_file(fn):
                s = dict(d)
                print(json.dumps(s, sort_keys=True, indent=2))

    @auto_help
    def do_author(self, args):
        from rengu.author import Author

        for fn in args.split():
            for d in Author.read_yaml_file(fn):
                a = dict(d)
                print(json.dumps(a, sort_keys=True, indent=2))

