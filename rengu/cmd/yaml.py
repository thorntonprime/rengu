import cmd

from rengu.cmd import auto_help
import yaml
from rengu.tools import YamlDumper

class RenguYAMLCmd(cmd.Cmd):

    prompt = "yaml >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_verse(self, args):
        from rengu.verse import Verse

        for fn in args.split():
            v = dict(Verse.read_yaml_file(fn))

            body = v["Body"].replace(":", "：")
            if body[0] == "'" or body[0] == '"' or body[0:3] == "...":
                body = "\\" + body

            del v["Body"]
            del v["Lines"]

            print("---")
            print(
                yaml.dump(
                    v,
                    Dumper=YamlDumper,
                    default_flow_style=False,
                    width=70,
                    indent=2).strip())
            print("---")
            print(body)

    @auto_help
    def do_source(self, args):
        from rengu.source import Source

        for fn in args.split():
            for d in Source.read_yaml_file(fn):
                s = dict(d)

                print("---")
                print(
                    yaml.dump(
                        s,
                        Dumper=YamlDumper,
                        default_flow_style=False,
                        width=70,
                        indent=2).strip())
        print("---")

    @auto_help
    def do_author(self, args):
        from rengu.author import Author

        for fn in args.split():
            for d in Author.read_yaml_file(fn):
                a = dict(d)

                print("---")
                print(
                    yaml.dump(
                        a,
                        Dumper=YamlDumper,
                        default_flow_style=False,
                        width=70,
                        indent=2).strip())

        print("---")
