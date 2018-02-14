

from pathlib import Path
from uuid import UUID

from blitzdb import Document, FileBackend

from rengu.verse import load_yaml_file, Verse

def load_all_yaml():

    backend = FileBackend("./db")

    verses_dir = Path('verses')
    for verse_file in verses_dir.iterdir():
        v = load_yaml_file(str(verse_file))
        v['pk'] = UUID(verse_file.name).hex

        backend.save(Verse(v))

    backend.commit()
