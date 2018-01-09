
from pathlib import Path

from uuid import UUID

import yaml

from blitzdb import Document, FileBackend

class Source(Document):
    pass

def load_all_yaml():

    backend = FileBackend("./db")

    sources_dir = Path('sources')
    for source_file in sources_dir.iterdir():
        for x in yaml.load_all(open(source_file).read()):
            if x:
                s = Source(x)
                s.attributes['_id'] = source_file.name
                s.pk = UUID(source_file.name).hex

        backend.save(s)

    backend.commit()

