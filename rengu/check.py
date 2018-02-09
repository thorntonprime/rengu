# import sys
# sys.path.append('')

import sys
from uuid import UUID

from blitzdb import FileBackend
from blitzdb.document import DoesNotExist, MultipleDocumentsReturned

from rengu.db.people import Person
from rengu.db.verses import Verse
from rengu.tools import check_roman, is_uuid

import spacy


# Set up globals
backend = FileBackend("./db")
nlp = spacy.load('en')


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
    except MultipleDocumentsReturned:
        print("Multiple people for %s ... this is broken." % (name))
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
        pass
        # print(uid, "BY_OK", by)

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


def check_similar_body(uid, body):

    body_doc = nlp(body)

    for other_verse in backend.filter(Verse, {}):

        other_uid = str(UUID(other_verse.pk))
        if uid == other_uid:
            continue

        other_body = str(other_verse.get('Body'))
        if other_body:
            other_body_doc = nlp(other_body)
            sim = body_doc.similarity(other_body_doc)
            if sim > .99:
                print(uid, "BODY_SIMILAR", sim, other_uid)


def check_similar_title(uid, title):

    title_doc = nlp(title)

    for other_verse in backend.filter(Verse, {}):

        other_uid = str(UUID(other_verse.pk))
        if uid == other_uid:
            continue

        other_title = str(other_verse.get('Title'))
        if other_title:
            other_title_doc = nlp(other_title)
            sim = title_doc.similarity(other_title_doc)
            if sim > .99:
                print(uid, "TITLE_SIMILAR", sim, other_uid)

def check_verse(verse):
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
            # check_similar_title(uid, title)


    # Skip body checks for now
    return

    # Check Body
    lang = verse.get('Lang')
    if lang and lang != 'en':
        print(uid, "LANG_NOTENGLISH", lang)

    body = verse.get('Body')
    if not body:
        print(uid, "BODY_MISSING")
    else:
        check_format(uid, "BODY", body)
        check_spelling(uid, "BODY", body)
        check_similar_body(uid, body)


def check_verses():

    for verse in backend.filter(Verse, {}):
        check_verse(verse)
        sys.stdout.flush()

