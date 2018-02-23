
import cmd

from rengu.cmd import auto_help


class RenguRefreshCmd(cmd.Cmd):

    prompt = "refresh >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_wikipedia(self, args):
        '''wikipedia
        Subcommands to import data from yaml files
        '''
        wikipedia_cmd = RenguRefreshWikipediaCmd()
        if len(args) > 1:
            return wikipedia_cmd.onecmd(args)
        else:
            return wikipedia_cmd.cmdloop()

    @auto_help
    def do_worldcat(self, args):
        '''worldcat
        Subcommands to reffresh data from worldcat
        '''
        worldcat_cmd = RenguRefreshWorldcatCmd()
        if len(args) > 1:
            return worldcat_cmd.onecmd(args)
        else:
            return worldcat_cmd.cmdloop()


class RenguRefreshWikipediaCmd(cmd.Cmd):

    prompt = "refresh wikipedia >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_author(self, args):
        '''author
        Refresh the Wikipedia data for the author record.
        '''

        from rengu.author import Author

        try:
            for pk in args.split():
                a = Author.fetch(pk)
                a.refresh_wikipedia()

        except SyntaxError as e:
            print(e)

    @auto_help
    def do_source(self, args):
        '''source
        Refresh the Wikipedia data for the source record.
        '''

        from rengu.source import Source

        try:
            for pk in args.split():
                s = Source.fetch(pk)
                s.refresh_wikipedia()

        except SyntaxError as e:
            print(e)


class RenguRefreshWorldcatCmd(cmd.Cmd):

    prompt = "refresh worldcat >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_source(self, args):
        '''source
        Refresh the W data for the source record.
        '''

        from rengu.source import Source

        try:
            for pk in args.split():
                s = Source.fetch(pk)
                ok = s.refresh_worldcat()

        except SyntaxError as e:
            print(e)
