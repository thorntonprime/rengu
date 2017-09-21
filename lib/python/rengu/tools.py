# -*- coding: utf-8 -*-

import unicodedata
import re

def strip_accents(s):
  return ''.join(c for c in unicodedata.normalize('NFD', s)
    if unicodedata.category(c) != 'Mn')

def remove_accents(input_str):
  nfkd_form = unicodedata.normalize('NFKD', input_str)
  return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def normalize(input_str):
  ## Returns a NFKD normalized form of the input string
  nfkd_form = unicodedata.normalize('NFKD', input_str)
  return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def mangle(input_str):
  # Returns an all-lower case NFKD normalized version of the input string with
  # all non-alpha characters removed
  d = unicodedata.normalize('NFKD', input_str).lower()
  return u"".join([ c for c in d if unicodedata.category(c) == 'Ll'])

numeral_map = tuple(zip(
    (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
    ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
))

def int_to_roman(i):
    result = []
    for integer, numeral in numeral_map:
        count = i // integer
        result.append(numeral * count)
        i -= integer * count
    return ''.join(result)

def check_roman(n):
  return re.match("^[MDCLXVI]+$",  n.upper())
  
def roman_to_int(n):
    if check_roman(n):
      i = result = 0
      for integer, numeral in numeral_map:
        while n[i:i + len(numeral)].upper() == numeral:
          result += integer
          i += len(numeral)
      return result
    else:
      return float('nan')
