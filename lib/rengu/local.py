# -*- coding: utf-8 -*-

import os

class Repository:

    def __init__(self, path=os.getenv("RENGUPATH", os.getcwd())):
        # Repository(RENGUPATH)
        #   Return a local repository object
        self.RENGU_PATH = path

    def updated_files(self):
        # updated_files()
        #   Return a generator of the updated (uncommitted) files in the local
        #   repository
        import sh
        for f in sh.git("-C", self.RENGU_PATH, "--no-pager", "diff", "--name-only"):
            yield f.strip()

    def updated_data(self):
        # updated_data()
        #   Return a generator of the updated (uncommitted) data files
        for (d,i) in (f.split("/", 1) for f in self.updated_files() if "/" in f):
                if d in ["authors", "sources", "verses"]:
                    yield "/".join(d,i)

    def push_all(self, msg):
        import sh
        git_all=sh.git("-C", self.RENGU_PATH, "commit", "-m", msg, *self.updated_files())

    def commit_data(self, msg):
        import sh
        git_all=sh.git("-C", self.RENGU_PATH, "commit", "-m", msg, *self.updated_files())


