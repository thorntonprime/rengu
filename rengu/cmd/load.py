
import cmd

from rengu.cmd import auto_help
from rengu.config import DB


class RenguLoadCmd(cmd.Cmd):

    prompt = "load >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_verse(self, args):
        from rengu.verse import Verse

        for fn in args.split():

            try:
                v = Verse.read_yaml_file(fn)
                print(v['pk'])
                v.save(DB)
            except Exception as e:
                import sys
                sys.stderr.write("Error reading %s\n" % (fn))
                sys.stderr.write("Error is %s\n" % (str(e)))
                sys.exit(1)

        DB.commit()

    @auto_help
    def do_source(self, args):
        from rengu.source import Source

        for fn in args.split():
            try:
                for s in Source.read_yaml_file(fn):
                    print(s['pk'])
                    s.save(DB)
            except Exception as e:
                import sys
                sys.stderr.write("Error reading %s\n" % (fn))
                sys.stderr.write("Error is %s\n" % (str(e)))
                sys.exit(1)

        DB.commit()

    @auto_help
    def do_author(self, args):
        from rengu.author import Author

        for fn in args.split():
            try:
                for a in Author.read_yaml_file(fn):
                    print(a['pk'])
                    a.save(DB)
            except Exception as e:
                import sys
                sys.stderr.write("Error reading %s\n" % (fn))
                sys.stderr.write("Error is %s\n" % (str(e)))
                sys.exit(1)

        DB.commit()
