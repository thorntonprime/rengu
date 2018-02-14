
import cmd

from rengu.cmd import auto_help

from rengu.config import DB

import yaml

from rengu.tools import YamlDumper

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
            v = DB.get(Verse, { "pk" : pk })

            body = v["Body"].replace(":", "：")
            if body[0] == "'" or body[0] == '"' or body[0:3] == "...":
                body = "\\" + body

            del v["Body"]
            del v["Lines"]

            print("---")
            print(
                yaml.dump(
                    dict(v),
                    Dumper=YamlDumper,
                    default_flow_style=False,
                    width=70,
                    indent=2).strip())
            print("---")
            print(body)

    @auto_help
    def do_source(self, args):
        from rengu.source import Source

        for pk in args.split():
            s = DB.get(Source, { "pk" : pk })

            print("---")
            print( yaml.dump(
                    dict(s),
                    Dumper=YamlDumper,
                        default_flow_style=False,
                        width=70,
                        indent=2).strip())
        print("---")


    @auto_help
    def do_author(self, args):
        from rengu.author import Author

        for pk in args.split():
            a = DB.get(Author, { "pk" : pk })

            print("---")
            print( yaml.dump(
                    dict(a),
                    Dumper=YamlDumper,
                        default_flow_style=False,
                        width=70,
                        indent=2).strip())
        print("---")

