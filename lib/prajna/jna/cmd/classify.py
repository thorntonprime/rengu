import cmd

from prajna.jna.cmd import auto_help
from prajna.jna.classify import load_classifier, dump_classifier, train, show

from prajna.jna.verse import Verse


class JnaClassifyCmd(cmd.Cmd):

    prompt = "classify >"

    @auto_help
    def do_quit(self, args):
        return True

    do_EOF = do_quit

    @auto_help
    def do_train(self, args):
        '''train pk [pk ...]
        Train the classifier with the body of the verse pk.
        '''
        cl = load_classifier()

        for pk in args.split():
            v = Verse.fetch(pk)
            for tag in train(cl, v):
                print(pk, tag)

        dump_classifier(cl)

    @auto_help
    def do_show(self, args):
        '''show pk [pk ...]
        Show the tags the classifier matches with the verse pk.
        '''
        cl = load_classifier()

        for pk in args.split():

            v = Verse.fetch(pk)
            for tag, prob in show(cl, v):
                print("{0} {1:0.6f} {2}".format(v.pk, prob, tag))
