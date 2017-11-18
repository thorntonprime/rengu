#!/usr/bin/python3

import sys

sys.path.append('lib/python')
import rengu.tools

if __name__ == '__main__':

  for l in sys.stdin.readlines():
    # print(rengu.tools.mangle(l),  rengu.tools.normalize(l))
    print(rengu.tools.normalize(l))
