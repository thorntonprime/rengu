# -*- coding: utf-8 -*-

import os
import sh

DATA_TYPES=["authors", "sources", "verses", "prints"]

class Repository:

    def __init__(self, path=os.getenv("RENGUPATH", os.getcwd())):
        # Repository(RENGUPATH)
        #   Return a local repository object

        if path == None:
            path=os.getenv("RENGUPATH", os.getcwd())

        self.RENGU_PATH = path
        self.git = sh.git.bake("-C", self.RENGU_PATH, "--no-pager", "-c", "color.ui=false")

    def repo_files(self, more=None, commit_ish='HEAD^:./'):
        try:
            # maybe use git ls-files?
            #for f in self.git("diff", "--no-commit-id", "--name-only", "-r", commit_ish, "--", *more if more else []  ):
            for f in self.git("diff", "--name-only", "--cached", "-r", commit_ish, "--", *more if more else []  ):
                yield f.strip()
        except sh.ErrorReturnCode_128 as e:
            print('Invalid repository path')
        except sh.ErrorReturnCode as e:
            print('Unspecified repository error')

    def updated_files(self):
         return self.repo_files()

    def all_data(self, data_types=DATA_TYPES):
        # all_data()
        #   Return a generator of all the data files
        for t in data_types:
            for p in os.listdir(os.path.join(self.RENGU_PATH, t)):
                    yield os.path.join(t,p)

    def updated_data(self):
        # updated_data()
        #   Return a generator of the updated (uncommitted) data files
        return self.repo_files(more=DATA_TYPES)

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


