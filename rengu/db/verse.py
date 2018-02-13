

from pathlib import Path
from uuid import UUID

from blitzdb import Document, FileBackend

from rengu.verse import load_yaml_file


class Verse(Document):

    class Meta(Document.Meta):
        primary_key = '_id'
        collection = 'verses'


def load_all_yaml():

    backend = FileBackend("./db")

    verses_dir = Path('verses')
    for verse_file in verses_dir.iterdir():
        v = load_yaml_file(str(verse_file))
        v['_id'] = UUID(verse_file.name).hex

        backend.save(Verse(v))

    backend.commit()
