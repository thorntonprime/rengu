
import cmd

from prajna.rengu.cmd import auto_help


class RenguSearchCmd(cmd.Cmd):

    prompt = "search >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_verse(self, args):
        from prajna.rengu.verse import Verse

        try:
            for v in Verse.search(args):
                print(v.to_json())
        except SyntaxError as e:
            print(e)

    @auto_help
    def do_source(self, args):
        from prajna.rengu.source import Source

        try:
            for s in Source.search(args):
                print(s.to_json())
        except SyntaxError as e:
            print(e)

    @auto_help
    def do_author(self, args):
        from prajna.rengu.author import Author

        try:
            for a in Author.search(args):
                print(a.to_json())

        except SyntaxError as e:
            print(e)
