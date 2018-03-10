# -*- coding: utf-8 -*-

from blitzdb import Document

from rengu.config import DB


class Source(Document):

    def to_yaml(self):
        import yaml
        from rengu.tools import YamlDumper

        return "---\n" + yaml.dump(dict(self),
                                   Dumper=YamlDumper, default_flow_style=False, allow_unicode=True,
                                   width=70, indent=2).strip() + "\n---"

    def to_json(self):
        import json

        return json.dumps(dict(self), sort_keys=True, indent=2)

    def refresh_wikipedia(self):
        import wptools
        import sys
        from io import StringIO

        page = None

        if self.get("Wikipedia") and self.get("Wikipedia").get("Base"):
            page = wptools.page(wikibase=self.get("Wikipedia").get("Base"),
                                silent=True, skip=['imageinfo'])
        elif self.get("Wikipedia") and self.get("Wikipedia").get("PageID"):
            page = wptools.page(pageid=self.get("Wikipedia").get("PageID"),
                                silent=True, skip=['imageinfo'])
        else:
            page = wptools.page(
                self.get("Title"), silent=True, skip=['imageinfo'])

        try:
            old_stderr = sys.stderr
            redirected_error = sys.stderr = StringIO()

            page.get(timeout=5)

        except LookupError:
            return False

        except Exception as e:
            raise e

        finally:
            sys.stderr = old_stderr

        if 'label' not in page.data:
            raise Exception("Wikipedia page with no label")

        # if page.data.get("what") != "human":
        #    print("%s WARN - Wikipedia author not human" % (self.pk))

        label = page.data.get("label")
        url = page.data.get("url").replace(" ", "_")
        wikibase = page.data.get("wikibase")
        pageid = page.data.get("pageid")
        what = page.data.get("what")

        if type(what) is tuple:
            what = ','.join(what)
        if what == 'Wikimedia disambiguation page':
            what = "(disambiguation)"

        if label != self.get("Title"):
            self['AlternateTitles'] = list(
                set(self.get("AlternateTitles", [])))

        self["Wikipedia"] = {
            "URL": url,
            "PageID": pageid,
            "Base": wikibase,
            "What": what
        }

        self.save(DB)
        DB.commit()

        return True

    def refresh_worldcat(self):
        from rengu.tools import walk
        from rengu.worldcat import search_isbn, search_title_author

        if self.get("Media", "").lower() in ["prime", "collection"]:
            raise Exception("incompatible media type")

        isbn = walk("ISBN", dict(self))
        if isbn:
            for i in isbn:
                data = search_isbn(i)
                if data:

                    self = Source({**self, **data})

                    self.save(DB)
                    DB.commit()

                    return True

        if self.get("Title") and self.get("By"):

            title = self.get("Title")
            author = self.get("By")
            if isinstance(author, list):
                author = author[0]

            data = search_title_author(title, author)
            if data:

                self = Source({**self, **data})

                self.save(DB)
                DB.commit()

                return True

        return False

    @staticmethod
    def fetch(pk):
        return DB.get(Source, {"pk": pk})

    @staticmethod
    def search(query):
        return DB.filter(Source, eval(query))

    @staticmethod
    def find(query, field="Title"):
        from rengu.tools import is_uuid

        found = set()

        if is_uuid(query):
            s = Source.fetch(query)
            yield s
            return

        if '/' in str(query):
            title, author = [x.strip() for x in query.split('/', 2)]
            for s in DB.filter(Source, {"Title": title, "By": author}):
                if s.pk not in found:
                    found.add(s.pk)
                    yield s

            for s in DB.filter(Source, {"AlternateTitles": title, "By": author}):
                if s.pk not in found:
                    found.add(s.pk)
                    yield s

        for s in DB.filter(Source, {field: query}):
            if s.pk not in found:
                found.add(s.pk)
                yield s

        if field == "Title":
            for s in DB.filter(Source, {"AlternateTitles": query}):
                if s.pk not in found:
                    found.add(s.pk)
                    yield s

    @staticmethod
    def read_yaml_file(fn):
        import yaml

        for data in yaml.load_all(open(fn).read()):
            if data:
                if not data.get('pk'):
                    from os.path import basename
                    data['pk'] = basename(fn)

                yield Source(data)

    class Meta(Document.Meta):
        primary_key = 'pk'
        collection = 'sources'


#####################################################################
# create indexes

from blitzdb.queryset import QuerySet

DB.create_index(Source, 'Title', fields={
                "Title": QuerySet.ASCENDING}, unique=False, ephemeral=False)
