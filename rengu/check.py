# import sys
# sys.path.append('')

from uuid import UUID

from blitzdb import FileBackend
from blitzdb.document import DoesNotExist

from rengu.tools import is_uuid

from rengu.db.verses import Verse
from rengu.db.people import Person

def find_person(name):

    backend = FileBackend("./db")
    person = None

    # name is actually a UUID
    if (is_uuid(name)):
        try:
            person = backend.get(Person, { '_id': UUID(name).hex })
        except DoesNotExist:
            person = None

        return person

    # Person is a real name
    try:
        person = backend.get(Person, { 'Name': name })
    except DoesNotExist:
        person = None

    # Or maybe an alternate name?
    if not person:
        try:
            person = backend.filter(Person, { 'AlternateNames': { '$in' : [name] } })[0]
        except IndexError:
            person = None
        except DoesNotExist:
            person = None

    return person 

def check_verses():

    backend = FileBackend("./db")

    for verse in backend.filter(Verse, {}):

        # Check By line
        if verse.get('By'):

            if isinstance(verse['By'], list):
                print(str(UUID(verse.pk)), verse['By'], " MULTIPLE AUTHORS")

                for p in verse['By']:
                    person = find_person(p)

                    if person: 
                        print(str(UUID(verse.pk)), p, " = ", person.Name)
                    else:
                        print(str(UUID(verse.pk)), p, " NO MATCH")

            else:
                person = find_person(verse['By'])

                if person: 
                    print(str(UUID(verse.pk)), verse['By'], " = ", person.Name)
                else:
                    print(str(UUID(verse.pk)), verse['By'], " NO MATCH")


