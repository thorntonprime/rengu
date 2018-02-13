
from pathlib import Path
from uuid import UUID

from blitzdb import Document, FileBackend

from rengu.author import load_yaml_file


class Author(Document):

    class Meta(Document.Meta):
        primary_key = '_id'
        collection = 'authors'


def load_all_yaml():

    backend = FileBackend("./db")

    authors_dir = Path('authors')
    for author_file in authors_dir.iterdir():

        p = load_yaml_file(str(author_file))
        p['_id'] = UUID(author_file.name).hex

        backend.save(Author(p))

    backend.commit()
