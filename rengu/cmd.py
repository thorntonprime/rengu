
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
    def do_people(self, line):
        '''people
        dump people referenced in verse files
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

        import rengu.db.people
        rengu.db.people.load_all_yaml()

        import rengu.db.sources
        rengu.db.sources.load_all_yaml()

        import rengu.db.verses
        rengu.db.verses.load_all_yaml()


