# -*- coding: utf-8 -*-

import re
import unicodedata
from collections import Iterable

from ftfy import fix_text

import yaml

numeral_map = tuple(zip(
    (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
    ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
))


class YamlDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(YamlDumper, self).increase_indent(flow, False)


def x_walk(match, d):
    '''walk( key to find, dictonary)
    recursively walk a dictonary to find a key
    and yield results
    '''
    # See also https://stackoverflow.com/questions/14962485/\
    #          finding-a-key-recursively-in-a-dictionary

    if not isinstance(d, dict):
        return

    for k in d.keys():

        if k == match:

            if isinstance(d[k], str):
                yield d[k]

            elif isinstance(d[k], list):
                for x in d[k]:
                    yield x

        elif isinstance(d[k], dict):
            for x in walk(match, d[k]):
                yield x

        elif isinstance(d[k], list):
            for x in (x for x in d[k] if isinstance(x, dict)):
                for y in walk(match, x):
                    yield y

def walk(key, d):
    '''walk( key to find, dictonary)
    recursively walk a dictonary to find a key
    and yield results
    '''

    if isinstance(d, dict):
        if key in d:
            yield d[key]

        for k in d:
            for i in  walk(key, d[k]):
                yield i

    if isinstance(d, list):
        for i in d:
            for j in walk(key, i):
                yield j


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', fix_text(s))
                   if unicodedata.category(c) != 'Mn')


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', fix_text(input_str))
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def normalize(input_str):
    # Returns a NFKD normalized form of the input string
    nfkd_form = unicodedata.normalize('NFKD', fix_text(input_str))
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def mangle(input_str):
    # Returns an all-lower case NFKD normalized version of the input string
    # with all non-alpha characters removed
    d = unicodedata.normalize('NFKD', fix_text(input_str)).lower()
    return u"".join([c for c in d if unicodedata.category(c) == 'Ll'])


def int_to_roman(i):
    result = []
    for integer, numeral in numeral_map:
        count = i // integer
        result.append(numeral * count)
        i -= integer * count
    return ''.join(result)


def check_roman(n):
    return re.match("^[MDCLXVI]+$", n.upper())


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


def flatten(items):
    """Yield items from any nested iterable; see REF."""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


def is_uuid(test):
    if not isinstance(test, str):
        return False

    if re.match("[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
                test):
        return True
    elif re.match("[0-9a-f]{32}", test):
        return True
    else:
        return False


def is_isbn(test):
    if re.match("[-0-9]+X?", test):
        return True
    else:
        return False


def lookup_wikipedia(article):
    import wptools

    page = wptools.page(normalize(article), silent=True, skip=['imageinfo'])
    try:
        page.get(timeout=5)
    except LookupError:
        page.data = {'what': "_error lookup_"}
        return page
    except RecursionError:
        page.data = {'what': "_error recusion_"}
        return page
    except:
        page.data = {'what': "_error other_"}
        return page

    if 'label' not in page.data:
        page.data = {'label': "_error no label_"}

    return page
