import cmd

from prajna.rengu.cmd import auto_help


class RenguJSONCmd(cmd.Cmd):

    prompt = "json >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_verse(self, args):
        from prajna.rengu.verse import Verse

        for fn in args.split():
            print(Verse.read_yaml_file(fn).to_json())

    @auto_help
    def do_source(self, args):
        from prajna.rengu.source import Source

        for fn in args.split():
            for s in Source.read_yaml_file(fn):
                print(s.to_json())

    @auto_help
    def do_author(self, args):
        from prajna.rengu.author import Author

        for fn in args.split():
            for a in Author.read_yaml_file(fn):
                print(a.to_json())
