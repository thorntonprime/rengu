
from pathlib import Path

from uuid import UUID

import yaml

from blitzdb import Document, FileBackend

from rengu.people import load_yaml_file

class Person(Document):
    pass

def load_all_yaml():

    backend = FileBackend("./db")

    people_dir = Path('people')
    for person_file in people_dir.iterdir():
        p = Person(load_yaml_file(str(person_file)))
        p.pk = UUID(person_file.name).hex

        backend.save(p)

    backend.commit()

