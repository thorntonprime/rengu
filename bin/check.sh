#!/bin/sh

rm -rf db
bin/rengu loaddb
bin/rengu check > output/check.out
grep NOMATCH output/check.out | sed -e 's/.*NOMATCH//' | sort | uniq | bin/wikipedia-make

