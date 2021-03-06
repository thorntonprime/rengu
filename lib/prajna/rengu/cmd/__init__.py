
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
        from prajna.rengu.cmd.load import RenguLoadCmd
        load_cmd = RenguLoadCmd()
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
        from prajna.rengu.cmd.extract import RenguExtractCmd
        extract_cmd = RenguExtractCmd()
        if len(args) > 1:
            return extract_cmd.onecmd(args)
        else:
            return extract_cmd.cmdloop()

    @auto_help
    def do_dump(self, args):
        '''dump
        Subcommands to import data from yaml files
        '''
        from prajna.rengu.cmd.dump import RenguDumpCmd
        dump_cmd = RenguDumpCmd()
        if len(args) > 1:
            return dump_cmd.onecmd(args)
        else:
            return dump_cmd.cmdloop()

    @auto_help
    def do_search(self, args):
        '''search
        Subcommands to search data using a search query
        '''
        from prajna.rengu.cmd.search import RenguSearchCmd
        search_cmd = RenguSearchCmd()
        if len(args) > 1:
            return search_cmd.onecmd(args)
        else:
            return search_cmd.cmdloop()

    @auto_help
    def do_find(self, args):
        '''find
        Subcommands to find data, matching the key field (e.g. name or title)
        '''
        from prajna.rengu.cmd.find import RenguFindCmd
        find_cmd = RenguFindCmd()
        if len(args) > 1:
            return find_cmd.onecmd(args)
        else:
            return find_cmd.cmdloop()

    @auto_help
    def do_fuzz(self, args):
        '''fuzz
        Subcommands to fuzz data, matching the key field (e.g. name or title)
        '''
        from prajna.rengu.cmd.fuzz import RenguFuzzCmd
        fuzz_cmd = RenguFuzzCmd()
        if len(args) > 1:
            return fuzz_cmd.onecmd(args)
        else:
            return fuzz_cmd.cmdloop()

    @auto_help
    def do_text(self, args):
        '''text
        Subcommands to index and search text data
        '''
        from prajna.rengu.cmd.text import RenguTextCmd
        text_cmd = RenguTextCmd()
        if len(args) > 1:
            return text_cmd.onecmd(args)
        else:
            return text_cmd.cmdloop()

    @auto_help
    def do_corpus(self, args):
        '''corpus
        Subcommands to manage corpus from Rengu verse data
        '''
        from prajna.rengu.cmd.corpus import RenguCorpusCmd
        corpus_cmd = RenguCorpusCmd()
        if len(args) > 1:
            return corpus_cmd.onecmd(args)
        else:
            return corpus_cmd.cmdloop()

    @auto_help
    def do_refresh(self, args):
        '''refresh
        Subcommands to refresh data from external sources
        '''
        from prajna.rengu.cmd.refresh import RenguRefreshCmd
        refresh_cmd = RenguRefreshCmd()
        if len(args) > 1:
            return refresh_cmd.onecmd(args)
        else:
            return refresh_cmd.cmdloop()

    @auto_help
    def do_similar(self, args):
        '''similar
        Subcommands to similar data from external sources
        '''
        from prajna.rengu.cmd.similar import RenguSimilarCmd
        similar_cmd = RenguSimilarCmd()
        if len(args) > 1:
            return similar_cmd.onecmd(args)
        else:
            return similar_cmd.cmdloop()

    @auto_help
    def do_json(self, args):
        '''json
        Subcommands to json data
        '''
        from prajna.rengu.cmd.json import RenguJSONCmd
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
        from prajna.rengu.cmd.yaml import RenguYAMLCmd
        yaml_cmd = RenguYAMLCmd()
        if len(args) > 1:
            return yaml_cmd.onecmd(args)
        else:
            return yaml_cmd.cmdloop()

    @auto_help
    def do_classify(self, args):
        '''classify
        Subcommands to classify data
        '''
        from prajna.rengu.cmd.classify import RenguClassifyCmd
        classify_cmd = RenguClassifyCmd()
        if len(args) > 1:
            return classify_cmd.onecmd(args)
        else:
            return classify_cmd.cmdloop()
