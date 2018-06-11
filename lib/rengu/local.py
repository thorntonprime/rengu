# -*- coding: utf-8 -*-

import os
import sh

DATA_TYPES=["authors", "sources", "verses"]

class Repository:

    def __init__(self, path=os.getenv("RENGUPATH", os.getcwd())):
        # Repository(RENGUPATH)
        #   Return a local repository object

        if path == None:
            path=os.getenv("RENGUPATH", os.getcwd())

        self.RENGU_PATH = path
        self.git = sh.git.bake("-C", self.RENGU_PATH, "--no-pager", "-c", "color.ui=false")

    def updated_files(self):
        # updated_files()
        #   Return a generator of the updated (uncommitted) files in the local
        #   repository
        #for f in self.git("diff", "--name-only"):
        try:
            for f in ( g[3:] for g in self.git("status", "--short")):
                yield f.strip()
        except sh.ErrorReturnCode_128 as e:
            print('Invalid repository path')
        except sh.ErrorReturnCode as e:
            print('Unspecified repository error')

    def all_data(self, data_types=DATA_TYPES):
        # all_data()
        #   Return a generator of all the data files
        for t in data_types:
            for p in os.listdir(os.path.join(self.RENGU_PATH, t)):
                    yield os.path.join(t,p)

    def updated_data(self):
        # updated_data()
        #   Return a generator of the updated (uncommitted) data files
        for (d,i) in (f.split("/", 1) for f in self.updated_files() if "/" in f):
                if d in ["authors", "sources", "verses"]:
                    yield "/".join([d,i])

    def commit_all(self, msg):
        self.git("commit", "-m", msg, *self.updated_files())

    def commit_data(self, msg):
        self.git("commit", "-m", msg, *self.updated_data())

    def push_commits(self):
        self.git("push")

    def push_data(self):
        self.commit_data("daily")
        self.push_commits()

class Cluster:

    def __init__(self):
        self.pdsh = sh.pdsh.bake("-g", "rengu", "-l", "rengu")

    def sync_all(self):
        print(self.pdsh("git", "pull"))


