
import cmd

from rengu.cmd import auto_help

from pprint import pprint

from rengu.config import DB

class RenguLoadCmd(cmd.Cmd):

    prompt = "load >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_verse(self, args):
        print("load verses")

    @auto_help
    def do_source(self, args):
        print("load sources")

    @auto_help
    def do_author(self, args):
        from rengu.author import Author

        for fn in args.split():
            
            for a in Author.read_yaml_file(fn):
                print("Loaded", a['pk'])
                a.save(DB)

        DB.commit()
