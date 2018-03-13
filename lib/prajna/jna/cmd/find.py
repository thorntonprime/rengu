
import cmd

from prajna.jna.cmd import auto_help


class JnaFindCmd(cmd.Cmd):

    prompt = "find >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_verse(self, args):
        from prajna.jna.verse import Verse

        try:
            for v in Verse.find(args):
                print(v.to_json())
        except SyntaxError as e:
            print(e)

    @auto_help
    def do_source(self, args):
        from prajna.jna.source import Source

        try:
            for s in Source.find(args):
                print(s.to_json())
        except SyntaxError as e:
            print(e)

    @auto_help
    def do_author(self, args):
        from prajna.jna.author import Author

        try:
            for a in Author.find(args):
                print(a.to_json())

        except SyntaxError as e:
            print(e)
