# -*- coding: utf-8 -*-

from blitzdb import Document

from rengu.config import DB


class Author(Document):

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
        import warnings
        page = None

        if self.get("Wikipedia") and self.get("Wikipedia").get("Base"):
            page = wptools.page(wikibase=self.get("Wikipedia").get("Base"),
                                silent=True, skip=['imageinfo'])
        elif self.get("Wikipedia") and self.get("Wikipedia").get("PageID"):
            page = wptools.page(pageid=self.get("Wikipedia").get("PageID"),
                                silent=True, skip=['imageinfo'])
        else:
            page = wptools.page(
                self.get("Name"), silent=True, skip=['imageinfo'])

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                page.get(timeout=5)

        except LookupError:
            print("%s ERROR - Wikipedia not found" % (self.pk))
            return

        except Exception as e:
            print("%s ERROR -  Wikipedia error %s" % (self.pk, e))
            return

        if 'label' not in page.data:
            print("%s ERROR - Wikipedia error no label" % (self.pk))
            return

        if page.data.get("what") != "human":
            print("%s WARN - Wikipedia author not human" % (self.pk))

        label = page.data.get("label")
        url = page.data.get("url").replace(" ", "_")
        wikibase = page.data.get("wikibase")
        pageid = page.data.get("pageid")
        what = page.data.get("what")

        if type(what) is tuple:
            what = ','.join(what)
        if what == 'Wikimedia disambiguation page':
            what = "(disambiguation)"

        if label != self.get("Name"):
            self['AlternateNames'] = list(set(self.get("AlternateNames", [])))

        self["Wikipedia"] = {
            "URL": url,
            "PageID": pageid,
            "Base": wikibase,
            "What": what
        }

        self.save(DB)
        DB.commit()
        print("%s OK" % (self.pk))

    @staticmethod
    def fetch(pk):
        return DB.get(Author, {"pk": pk})

    @staticmethod
    def search(query):
        return DB.filter(Author, eval(query))

    @staticmethod
    def find(query, field="Name"):

        found = set()

        for a in DB.filter(Author, {field: query}):
            if a.pk not in found:
                found.add(a.pk)
                yield a

        if field == "Name":
            for a in DB.filter(Author, {"AlternateNames": query}):
                if a.pk not in found:
                    found.add(a.pk)
                    yield a

    @staticmethod
    def read_yaml_file(fn):
        import yaml

        for data in yaml.load_all(open(fn).read()):
            if data:
                if not data.get('pk'):
                    from os.path import basename
                    data['pk'] = basename(fn)

                yield Author(data)

    # Class internal data and methods ###############################
    class Meta(Document.Meta):
        primary_key = 'pk'
        collection = 'authors'


#####################################################################
# Create Indexes
from blitzdb.queryset import QuerySet

DB.create_index(Author, 'Name', fields={
                "Name": QuerySet.ASCENDING}, unique=True, ephemeral=False)
DB.create_index(Author, 'AlternateNames', fields={
                "AlternateNames": QuerySet.ASCENDING},
                unique=True, ephemeral=False)
