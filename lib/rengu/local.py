# -*- coding: utf-8 -*-

import os

class Repository:

    def __init__(self, path=os.getenv("RENGUPATH", os.getcwd())):
        # Repository(RENGUPATH)
        #   Return a local repository object
        import sh

        self.RENGU_PATH = path
        self.git = sh.git.bake("-C", self.RENGU_PATH, "--no-pager")

    def updated_files(self):
        # updated_files()
        #   Return a generator of the updated (uncommitted) files in the local
        #   repository
        for f in self.git("diff", "--name-only"):
            yield f.strip()

    def updated_data(self):
        # updated_data()
        #   Return a generator of the updated (uncommitted) data files
        for (d,i) in (f.split("/", 1) for f in self.updated_files() if "/" in f):
                if d in ["authors", "sources", "verses"]:
                    yield "/".join(d,i)

    def commit_all(self, msg):
        self.git("commit", "-m", msg, *self.updated_files())

    def commit_data(self, msg):
        self.git("commit", "-m", msg, *self.updated_data())

    def push_commits(self):
        self.git("push")

    def push_data(self):
        self.commit_data("daily")
        self.push_commits()

