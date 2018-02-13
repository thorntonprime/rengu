
import cmd

import rengu.verse
from rengu.tools import YamlDumper, walk_search


def auto_help(func):
    def _help(self):
        print(func.func_doc)
    setattr(cmd.Cmd, 'help_' + func.__name__[3:], _help)
    return func

class RenguCmd(cmd.Cmd, object):
    intro = 'Rengu tool'
    prompt = '> '

    @auto_help
    def do_quit(self, args):
        '''quit
        Quit the tool
        '''
        return True
    do_EOF = do_quit

    @auto_help
    def do_load(self, args):
        '''load
        Subcommands to import data from yaml files
        '''
        from rengu.cmd.load import RenguLoadCmd
        load_cmd = RenguLoadCmd()
        if len(args) > 1:
            return load_cmd.onecmd(args)
        else:
            return load_cmd.cmdloop()

    @auto_help
    def do_find(self, args):
        '''find
        Subcommands to find data
        '''
        from rengu.cmd.find import RenguFindCmd
        find_cmd = RenguFindCmd()
        if len(args) > 1:
            return find_cmd.onecmd(args)
        else:
            return find_cmd.cmdloop()

    ###################

    @auto_help
    def do_dumpfile(self, line):
        '''dumpfile
        dump file in a flat format with dot names
        '''

        for f in line.split():
            rdoc = rengu.verse.load_yaml_file(f)

            print(rdoc)

    @auto_help
    def do_json(self, line):
        '''json
        dump verse data in JSON
        '''

        import json
        for f in line.split():
            rdoc = rengu.verse.load_yaml_file(f)
            print(json.dumps(rdoc, sort_keys=True, indent=2))

    @auto_help
    def do_yaml(self, line):
        '''yaml
        dump verse data in YAML
        '''

        import yaml
        for f in line.split():
            rdoc = rengu.verse.load_yaml_file(f)

            body = rdoc["Body"]
            if body[0] == "'" or body[0] == '"' or body[0:3] == "...":
                body = "\\" + body

            del rdoc["Body"]
            del rdoc["Lines"]
            # del rdoc["_id"]

            # Temporary fix for Description
            month = [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December"]
            for x in month:
                if rdoc.get("Description") and rdoc[
                        "Description"][0:len(x)] == x:
                    rdoc["Source"].setdefault("Locus", {}).update(
                        {"Daily": rdoc["Description"]})
                    del rdoc["Description"]
                    break

            print("---")
            print(
                yaml.dump(
                    rdoc,
                    Dumper=YamlDumper,
                    default_flow_style=False,
                    width=70,
                    indent=2).strip())
            print("---")
            print(body.replace(":", "："))

    @auto_help
    def do_authors(self, line):
        '''authors
        dump authors referenced in verse files
        '''

        for f in line.split():
            rdoc = rengu.verse.load_yaml_file(f)

            for t in walk_search('By', rdoc):
                print(t)

    @auto_help
    def do_sources(self, line):
        '''sources
        dump source titles referenced in verse files
        '''

        for f in line.split():
            rdoc = rengu.verse.load_yaml_file(f)

            for t in walk_search('Title', rdoc.get('Source', {})):
                print(t)

            for t in walk_search('Title', rdoc.get('References', {})):
                print(t)

    @auto_help
    def do_tags(self, line):
        '''tags
        dump tags referenced in verse files
        '''

        for f in line.split():
            rdoc = rengu.verse.load_yaml_file(f)

            for t in walk_search('Tags', rdoc):
                print(t)

    @auto_help
    def do_loaddb(self, line):
        '''loaddb
        Load the YAML files into the blitzdb
        '''

        import rengu.db.author
        # backend.create_index(Author, params="Name", unique=True )
        # backend.rebuild_index('authors', key="Name")
        rengu.db.author.load_all_yaml()

        import rengu.db.source
        rengu.db.source.load_all_yaml()

        import rengu.db.verse
        rengu.db.verse.load_all_yaml()

    @auto_help
    def do_authorsmap(self, line):
        '''authorsmap
        Load authors map
        '''

        import rengu.author
        authors_map = rengu.author.load_authors_map()

        import json
        print(json.dumps(authors_map, sort_keys=True, indent=2))

    @auto_help
    def do_check(self, line):
        '''check
        Check all the YAML files
        '''

        import rengu.check
        rengu.check.check_verses()
