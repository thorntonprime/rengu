
from pathlib import Path
from uuid import UUID

from blitzdb import Document, FileBackend

from rengu.author import load_yaml_file, Author


def load_all_yaml():

    backend = FileBackend("./db")

    authors_dir = Path('authors')
    for author_file in authors_dir.iterdir():

        p = load_yaml_file(str(author_file))
        p['pk'] = UUID(author_file.name).hex

        backend.save(Author(p))

    backend.commit()
