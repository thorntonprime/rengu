# -*- coding: utf-8 -*-

ROMAN = tuple(zip(
    (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
    ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
))

def int_to_roman(i):
  result = []
  for integer, numeral in ROMAN:
    count = i // integer
    result.append(numeral * count)
    i -= integer * count
  return ''.join(result)

def roman_to_int(n):
  i = result = 0
  for integer, numeral in ROMAN:
     while n[i:i + len(numeral)].upper() == numeral:
       result += integer
       i += len(numeral)
       continue
  return result

def normalize(x):
  '''normalize(x)
     Convert x to a normal form for comparison
  '''

  # Or the final scope value can be a sequence
  if isinstance(x, str) and "," in x:
    return [ normalize(y) for y in x.split(",") ]
      
  # The final scope value can be a range
  if isinstance(x, str) and "-" in x:
    v,w = x.split("-", 2)
    
    if v.isdigit() and w.isdigit():
      return list(range(int(v),int(w)))

    if roman_to_int(v) and roman_to_int(w):
      return list(range(roman_to_int(v),roman_to_int(w)))

  if isinstance(x, str) and roman_to_int(x):
    return roman_to_int(x)

  if isinstance(x, str) and x.isdigit():
    return int(x)

  return x



class Locus(object):
  '''Locus(orig)
     Class to manage Locus.
  '''

  # Scopes named from smallest to largest
  SCOPES = [ 'Series', 'Book', 'Volume', 'Part', 'Chapter', 'Section', 'Verse' ]
  _d = {}

  def __init__(self, x):

    # The scopes are pasted in reverse order as x, so largest to smallest

    # Unpack values
    if isinstance(x, dict):
      self._d = x
    elif isinstance(x, list):
      self._d = dict(zip(reversed(self.SCOPES), reversed(x)))
    elif isinstance(x, str):
      self._d = dict(zip(reversed(self.SCOPES), reversed(x.split())))


  def __repr__(self):
    from pprint import pformat
    return pformat(self._d)

  def __lt__(self, other):

    assert isinstance(other, Locus)

    for k in self.SCOPES:
      mine = normalize(self._d.get(k, 0))
      theirs = normalize(other._d.get(k, 0))

      if type(mine) != type(theirs):
        mine = str(mine)
        theirs = str(theirs)

      if mine < theirs:
        return True

      elif mine > theirs:
        return False 

    return False
    
  def __eq__(self, other):

    assert isinstance(other, Locus)

    for k in self.SCOPES:
      mine = normalize(self._d.get(k, 0))
      theirs = normalize(other._d.get(k, 0))

      if type(mine) != type(theirs):
        return False

      if mine != theirs:
        return False

    return True 

  def __contains__(self, item):

    assert isinstance(item, Locus)

    for k in self.SCOPES:
      mine = normalize(self._d.get(k))
      theirs = normalize(item._d.get(k))

      # If both are the same (including None), skip to next scope
      if mine == theirs:
        continue
 
      # If theirs is None and mine isn't, then they are broader
      if theirs == None:
        return False

      # if mine is None and theirs isn't, then I am broader
      if mine == None:
        return True
 
      # Check for list membership
      if not isinstance(mine, list):
        return False 

      elif isinstance(theirs, list):
        return set(theirs).issubset(mine)

      elif theirs in mine:
        return True

      else:
        return False

    # Default is true
    return True 

class BibleLocus(Locus):
  '''BibleLocus(orig)
     Class to manage BibleLocus.
  '''

  SCOPES = [ 'Book', 'Chapter', 'Verse' ]


