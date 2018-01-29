# import sys
# sys.path.append('')

from uuid import UUID

from blitzdb import FileBackend
from blitzdb.document import DoesNotExist

from rengu.db.people import Person
from rengu.db.verses import Verse
from rengu.tools import is_uuid, check_roman


def find_person(backend, name):

    person = None

    # name is actually a UUID
    if (is_uuid(name)):
        try:
            person = backend.get(Person, {'_id': UUID(name).hex})
        except DoesNotExist:
            person = None

        return person

    # Person is a real name
    try:
        person = backend.get(Person, {'Name': name})
    except DoesNotExist:
        person = None

    # Or maybe an alternate name?
    if not person:
        try:
            person = backend.filter(
                Person, {'AlternateNames': {'$in': [name]}})[0]
        except IndexError:
            person = None
        except DoesNotExist:
            person = None

    return person


def check_By(backend, uid, by):

    if not by:
        print(uid, "BY_MISSING")
        return

    if isinstance(by, list):
        print(uid, "BY_MULTIPLE")
        for n in by:
            check_By(backend, uid, n)
            return

    person = find_person(backend, by)

    if not person:
        print(uid, "BY_NOMATCH", by)

    elif person.Name != by:
        print(uid, "BY_NAME", by, "!=", person.Name)

    elif person.Name == by:
        print(uid, "BY_OK", by)

    else:
        print(uid, "BY_ERROR", by)

    return

def check_spelling(uid, cat, text):
    from enchant import DictWithPWL
    from enchant.checker import SpellChecker

    dictionary = DictWithPWL("en_US", "maps/words.txt")
    checker = SpellChecker(dictionary)

    checker.set_text(text)
    for error in checker:
        print(uid, cat + "_SPELL", error.word)

def check_format(uid, cat, text):
    import re
    
    # Check for bad capitalization
    for m in re.finditer("[A-Z][A-Z]+", text):
        if not check_roman(m.group(0)):
            print(uid, cat + "_FORMAT", m.group(0), text)


def check_verses():

    backend = FileBackend("./db")

    for verse in backend.filter(Verse, {}):

        uid = str(UUID(verse.pk))

        # Check By 
        by = verse.get('By')
        check_By(backend, uid, by)

        # Check Title
        title = verse.get('Title')
        if title:
            if not isinstance(title, str):
                print(uid, "TITLE_NOTSTR", title)
            else:
                check_format(uid, "TITLE", title)
                check_spelling(uid, "TITLE", title)

