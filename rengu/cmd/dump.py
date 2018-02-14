
import cmd

from rengu.cmd import auto_help


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
            print(Verse.fetch(pk).to_yaml())

    @auto_help
    def do_source(self, args):
        from rengu.source import Source

        for pk in args.split():
            print(Source.fetch(pk).to_yaml())


    @auto_help
    def do_author(self, args):
        from rengu.author import Author

        for pk in args.split():
            print(Author.fetch(pk).to_yaml())

