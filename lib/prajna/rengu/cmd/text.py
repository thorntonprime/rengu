import cmd

from prajna.rengu.cmd import auto_help
import prajna.rengu.text
from prajna.rengu.config import XDBPATH

class RenguTextCmd(cmd.Cmd):

    prompt = "text >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_index(self, args):
        '''index [verse_id ...]
        Full text index of the specified verses
        '''
        from prajna.rengu.verse import Verse
        import xapian

        xapiandb = prajna.rengu.text._get_xapian_db(XDBPATH, writeable=True)

        for pk in args.split():
            v = Verse.fetch(pk)
            prajna.rengu.text.index(xapiandb, v)
            print(pk)

        xapiandb.close()

    @auto_help
    def do_search(self, args):
        '''search <search terms>
        Full text search of the verse bodies.
        '''
        
        import xapian
        xapiandb = prajna.rengu.text._get_xapian_db(XDBPATH)

        try:
            for n, pct, pk, line in prajna.rengu.text.search(xapiandb, args):
                print("{0:3} {1} {2:.70}".format(pct, pk, line))
        except BrokenPipeError:
            pass

        finally:
            xapiandb.close()
