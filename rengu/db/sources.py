
from pathlib import Path

from uuid import UUID

import yaml

from blitzdb import Document, FileBackend

from rengu.sources import load_yaml_file

class Source(Document):
    pass

def load_all_yaml():

    backend = FileBackend("./db")

    sources_dir = Path('sources')
    for source_file in sources_dir.iterdir():
        s = Source(load_yaml_file(str(source_file)))
        s.pk = UUID(source_file.name).hex

        backend.save(s)

    backend.commit()

