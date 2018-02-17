# -*- coding: utf-8 -*-

from blitzdb import Document
from rengu.config import DB


class Source(Document):

    def to_yaml(self):
        import yaml
        from rengu.tools import YamlDumper

        return "---\n" + yaml.dump(dict(self),
                                   Dumper=YamlDumper, default_flow_style=False,
                                   width=70, indent=2).strip() + "\n---"

    def to_json(self):
        import json

        return json.dumps(dict(self), sort_keys=True, indent=2)

    def refresh_wikipedia(self):
        import wptools
        import urllib.parse
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
                self.get("Title"), silent=True, skip=['imageinfo'])

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

        if not 'label' in page.data:
            print("%s ERROR - Wikipedia error no label" % (self.pk))
            return

        #if page.data.get("what") != "human":
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
            self['AlternateTitles'] = list(set(self.get("AlternateTitles", [])))

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
        return DB.get(Source, {"pk": pk})

    @staticmethod
    def search(query):
        return DB.filter(Source, eval(query))

    @staticmethod
    def find(query, field="Title"):

        found = set()

        for a in DB.filter(Source, {field: query}):
            if not a.pk in found:
                found.add(a.pk)
                yield a

        if field == "Title":
            for a in DB.filter(Source, {"AlternateTitles": query}):
                if not a.pk in found:
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

                yield Source(data)

    class Meta(Document.Meta):
        primary_key = 'pk'
        collection = 'sources'

from blitzdb.queryset import QuerySet
DB.create_index(Source, 'Title', fields={
                "Title": QuerySet.ASCENDING}, unique=False, ephemeral=False)
