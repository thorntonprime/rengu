
from pathlib import Path
from uuid import UUID

from blitzdb import Document, FileBackend

from rengu.people import load_yaml_file


class Person(Document):

    class Meta(Document.Meta):
        primary_key = '_id'


def load_all_yaml():

    backend = FileBackend("./db")

    people_dir = Path('people')
    for person_file in people_dir.iterdir():

        p = load_yaml_file(str(person_file))
        p['_id'] = UUID(person_file.name).hex

        backend.save(Person(p))

    backend.commit()
