
from pathlib import Path
from uuid import UUID

from blitzdb import Document, FileBackend

from rengu.sources import load_yaml_file


class Source(Document):

    class Meta(Document.Meta):
        primary_key = '_id'
        collection = 'sources'


def load_all_yaml():

    backend = FileBackend("./db")

    sources_dir = Path('sources')
    for source_file in sources_dir.iterdir():
        s = load_yaml_file(str(source_file))
        s['_id'] = UUID(source_file.name).hex

        backend.save(Source(s))

    backend.commit()
