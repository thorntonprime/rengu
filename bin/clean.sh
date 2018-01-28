#!/bin/sh

rm -rf db
bin/rengu loaddb
bin/rengu check > tmp/check.out
grep NOMATCH tmp/check.out | sed -e 's/.*NOMATCH//' | sort | uniq | bin/wikipedia-make

