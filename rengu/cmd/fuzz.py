
import cmd

from rengu.cmd import auto_help


class RenguFuzzCmd(cmd.Cmd):

    prompt = "fuzz >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_author(self, args):
        import json
        from rengu.author import Author
        from operator import itemgetter

        try:
            matches = sorted(Author.fuzz(args), key=itemgetter('Match'))
            if len(matches) > 0:
                print(json.dumps(matches, sort_keys=True, indent=2))

        except SyntaxError as e:
            print(e)

