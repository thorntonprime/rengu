
import cmd


def auto_help(func):
    def _help(self):
        print(func.func_doc)
    setattr(cmd.Cmd, 'help_' + func.__name__[3:], _help)
    return func


class JnaCmd(cmd.Cmd, object):
    intro = 'Jna tool'
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
        from prajna.jna.cmd.load import JnaLoadCmd
        load_cmd = JnaLoadCmd()
        if len(args) > 1:
            return load_cmd.onecmd(args)
        else:
            return load_cmd.cmdloop()

    @auto_help
    def do_extract(self, args):
        '''extract
        Subcommands to extract associated info.
        It recursively will extract information on authors or sources from
        verses.
        '''
        from prajna.jna.cmd.extract import JnaExtractCmd
        extract_cmd = JnaExtractCmd()
        if len(args) > 1:
            return extract_cmd.onecmd(args)
        else:
            return extract_cmd.cmdloop()

    @auto_help
    def do_dump(self, args):
        '''dump
        Subcommands to import data from yaml files
        '''
        from prajna.jna.cmd.dump import JnaDumpCmd
        dump_cmd = JnaDumpCmd()
        if len(args) > 1:
            return dump_cmd.onecmd(args)
        else:
            return dump_cmd.cmdloop()

    @auto_help
    def do_search(self, args):
        '''search
        Subcommands to search data using a search query
        '''
        from prajna.jna.cmd.search import JnaSearchCmd
        search_cmd = JnaSearchCmd()
        if len(args) > 1:
            return search_cmd.onecmd(args)
        else:
            return search_cmd.cmdloop()

    @auto_help
    def do_find(self, args):
        '''find
        Subcommands to find data, matching the key field (e.g. name or title)
        '''
        from prajna.jna.cmd.find import JnaFindCmd
        find_cmd = JnaFindCmd()
        if len(args) > 1:
            return find_cmd.onecmd(args)
        else:
            return find_cmd.cmdloop()

    @auto_help
    def do_corpus(self, args):
        '''corpus
        Subcommands to manage corpus from Jna verse data
        '''
        from prajna.jna.cmd.corpus import JnaCorpusCmd
        corpus_cmd = JnaCorpusCmd()
        if len(args) > 1:
            return corpus_cmd.onecmd(args)
        else:
            return corpus_cmd.cmdloop()

    @auto_help
    def do_refresh(self, args):
        '''refresh
        Subcommands to refresh data from external sources
        '''
        from prajna.jna.cmd.refresh import JnaRefreshCmd
        refresh_cmd = JnaRefreshCmd()
        if len(args) > 1:
            return refresh_cmd.onecmd(args)
        else:
            return refresh_cmd.cmdloop()

    @auto_help
    def do_similar(self, args):
        '''similar
        Subcommands to similar data from external sources
        '''
        from prajna.jna.cmd.similar import JnaSimilarCmd
        similar_cmd = JnaSimilarCmd()
        if len(args) > 1:
            return similar_cmd.onecmd(args)
        else:
            return similar_cmd.cmdloop()

    @auto_help
    def do_json(self, args):
        '''json
        Subcommands to json data
        '''
        from prajna.jna.cmd.json import JnaJSONCmd
        json_cmd = JnaJSONCmd()
        if len(args) > 1:
            return json_cmd.onecmd(args)
        else:
            return json_cmd.cmdloop()

    @auto_help
    def do_yaml(self, args):
        '''yaml
        Subcommands to yaml data
        '''
        from prajna.jna.cmd.yaml import JnaYAMLCmd
        yaml_cmd = JnaYAMLCmd()
        if len(args) > 1:
            return yaml_cmd.onecmd(args)
        else:
            return yaml_cmd.cmdloop()

    @auto_help
    def do_classify(self, args):
        '''classify
        Subcommands to classify data
        '''
        from prajna.jna.cmd.classify import JnaClassifyCmd
        classify_cmd = JnaClassifyCmd()
        if len(args) > 1:
            return classify_cmd.onecmd(args)
        else:
            return classify_cmd.cmdloop()
