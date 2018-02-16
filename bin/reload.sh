#!/bin/sh

# Pre-Checks
echo "Runing Pre-Checks"
yamllint -f parsable verses/* authors/* sources/* | tee output/yaml.check

# Clear and Load Data
echo "Clearing and loading data"
rm -rf db
bin/rengu load verse verses/* > output/verses.load
bin/rengu load source sources/* > output/sources.load
bin/rengu load author authors/* > output/authors.load

# Post-Checks
echo "Running Post-checks"
echo " ... authors extract"
(
  bin/rengu search verse '{}' | \
    jq -r .pk | \
    xargs bin/rengu-extract-authors verse

  bin/rengu search source '{}' | \
    jq -r .pk | \
    xargs bin/rengu-extract-authors source
) | \
  sort | uniq -c | tee output/author.list | \
  cut -c9- | \
  bin/rengu-check-author > output/author.check

echo " ... titles extract"
bin/rengu search verse '{}' | \
  jq -r .pk | \
  xargs bin/rengu-extract-source | \
  sort | uniq -c | sort -g > output/titles.list

echo " ... fuzz authors"
cat output/author.check | grep 'NO MATCH' | \
  cut -d'!' -f 1 | \
  bin/rengu-fuzz-author > output/author.fuzz

# Fix-Ups
echo " ... wikilookup authors"
cat output/author.check | grep 'NO MATCH' | \
  cut -d'!' -f 1 | tr -d "'" | \
  bin/wikipedia-make

