
import cmd


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
    def do_dump(self, args):
        '''dump
        Subcommands to import data from yaml files
        '''
        from rengu.cmd.dump import RenguDumpCmd
        dump_cmd = RenguDumpCmd()
        if len(args) > 1:
            return dump_cmd.onecmd(args)
        else:
            return dump_cmd.cmdloop()

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

    @auto_help
    def do_json(self, args):
        '''json
        Subcommands to json data
        '''
        from rengu.cmd.json import RenguJSONCmd
        json_cmd = RenguJSONCmd()
        if len(args) > 1:
            return json_cmd.onecmd(args)
        else:
            return json_cmd.cmdloop()

    @auto_help
    def do_yaml(self, args):
        '''yaml
        Subcommands to yaml data
        '''
        from rengu.cmd.yaml import RenguYAMLCmd
        yaml_cmd = RenguYAMLCmd()
        if len(args) > 1:
            return yaml_cmd.onecmd(args)
        else:
            return yaml_cmd.cmdloop()

    ###################

    @auto_help
    def do_check(self, line):
        '''check
        Check all the YAML files
        '''

        import rengu.check
        rengu.check.check_verses()
