
import cmd

from prajna.rengu.cmd import auto_help


class RenguFuzzCmd(cmd.Cmd):

    prompt = "fuzz >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_source(self, args):
        from prajna.rengu.source import Source

        try:
            for s in Source.find(args):
                print(s.to_json())
        except SyntaxError as e:
            print(e)

    @auto_help
    def do_author(self, args):
        import shlex
        from prajna.rengu.author import Author

        author_map = Author.author_map()

        for name in shlex.split(args):
            for f, pk, match_name, real_name in Author.fuzz(name, match_ratio=80, authors=author_map):
                print("{0: 3g} {1:50} = {2:25} [{3}]".format(f, name + "~" +match_name, real_name, pk))

