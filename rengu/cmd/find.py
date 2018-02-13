
import cmd

import rengu.config
from rengu.cmd import auto_help


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
        print("find authors")
