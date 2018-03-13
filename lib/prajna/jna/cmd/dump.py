
import cmd

from prajna.jna.cmd import auto_help


class JnaDumpCmd(cmd.Cmd):

    prompt = "dump >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_verse(self, args):
        from prajna.jna.verse import Verse

        for pk in args.split():
            print(Verse.fetch(pk).to_yaml())

    @auto_help
    def do_source(self, args):
        from prajna.jna.source import Source

        for pk in args.split():
            print(Source.fetch(pk).to_yaml())

    @auto_help
    def do_author(self, args):
        from prajna.jna.author import Author

        for pk in args.split():
            print(Author.fetch(pk).to_yaml())
