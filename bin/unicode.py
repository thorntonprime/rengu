#!/usr/bin/python3

import unicodedata

def strip_accents(s):
  return ''.join(c for c in unicodedata.normalize('NFD', s)
    if unicodedata.category(c) != 'Mn')

def remove_accents(input_str):
  nfkd_form = unicodedata.normalize('NFKD', input_str)
  return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

if __name__ == '__main__':
  import sys

  print(remove_accents(sys.stdin.read()).rstrip())

