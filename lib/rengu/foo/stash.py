#!/usr/bin/env python3

import os
import sys

RENGUPATH=os.environ.get("RENGUPATH")
if not RENGUPATH:
  RENGUPATH=os.getcwd()


if os.access(RENGUPATH + "/bin/CONFIG", os.R_OK):
    with open(RENGUPATH + "/bin/CONFIG") as config:
      exec(config.read())
else:
    print("Couldn't find RENGU in " + RENGUPATH)
    sys.exit(1)

sys.path.append(RENGUPATH + '/lib')

from signal import signal, SIGPIPE, SIG_DFL 
#Ignore SIG_PIPE and don't throw exceptions on it... (http://docs.python.org/library/signal.html)
signal(SIGPIPE,SIG_DFL) 

import rengu.local

#r = rengu.local.Repository("/home/thornton/projects/rengu")
r = rengu.local.Repository(RENGUPATH)

for x in r.updated_data():
    print(x)
    import rengu.check
    for e in rengu.check.lint(open(x, 'r')):
        print(x, e)

#r.commit_all("Daily")
#r.push_commits()

#c=rengu.local.Cluster()
#c.sync_all()

