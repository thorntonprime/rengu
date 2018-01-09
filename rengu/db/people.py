
from pathlib import Path

from uuid import UUID

import yaml

from blitzdb import Document, FileBackend

class Person(Document):
    pass

def load_all_yaml():

    backend = FileBackend("./db")

    people_dir = Path('people')
    for person_file in people_dir.iterdir():
        for x in yaml.load_all(open(person_file).read()):
            if x:
                p = Person(x)
                p.attributes['_id'] = person_file.name
                p.pk = UUID(person_file.name).hex

        backend.save(p)

    backend.commit()

