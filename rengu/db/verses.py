

from pathlib import Path

from uuid import UUID

from blitzdb import Document, FileBackend

from rengu.verse import load_yaml_file

class Verse(Document):
    pass

def load_all_yaml():

    backend = FileBackend("./db")

    verses_dir = Path('verses')
    for verse_file in verses_dir.iterdir():
        x = load_yaml_file(str(verse_file))
        v = Verse(x)
        v.pk = UUID(verse_file.name).hex

        backend.save(v)

    backend.commit()

