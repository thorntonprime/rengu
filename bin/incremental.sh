#!/bin/sh

# Pre-Checks
echo "Running Pre-Checks"
yamllint -f parsable verses/* authors/* sources/* | tee output/yaml.check

# Incrementals

# Clear and Load Data
echo "Loading incremental"
git status | grep 'verses/' | sed -e 's@ *verses/@@' | \
  tee output/verses.incr | \
  xargs bin/rengu load verse verses/* >> output/verses.load

git status | grep 'sources/' | sed -e 's@ *sources/@@' | \
  tee output/sources.incr | \
  xargs bin/rengu load source sources/* >> output/sources.load

git status | grep 'authors/' | sed -e 's@ *authors/@@' | \
  tee output/sources.incr | \
  xargs bin/rengu load author authors/* >> output/authors.load


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

  bin/rengu search author '{}' | \
    jq -r .Members[]? 
) | \
  sort | uniq -c | tee output/authors.list | \
  cut -c9- | \
  bin/rengu-exists-author > output/authors.exists

echo " ... titles extract"
bin/rengu search verse '{}' | \
  jq -r .pk | \
  xargs bin/rengu-extract-title | \
  sort | uniq -c | sort -g > output/titles.list

echo " ... fuzz authors"
cat output/authors.exists | grep 'NO MATCH' | \
  cut -d'!' -f 1 | \
  bin/rengu-fuzz-author > output/authors.fuzz

echo " ... exists titles"
cat output/titles.list | cut -c9- | \
  bin/rengu-exists-source  > output/titles.exists

echo " ... fuzz titles"
cat output/titles.exists | grep 'NO MATCH' | \
  cut -d'!' -f 1 | \
  bin/rengu-fuzz-title > output/titles.fuzz

echo " ... fix verses"
bin/rengu search verse '{}' | jq -r .pk | \
  xargs bin/rengu-fix-verse > output/verses.fix

exit
############################ END

# Fix-Ups
echo " ... wikilookup authors"
cat output/authors.exists | grep 'NO MATCH' | \
  cut -d'!' -f 1 | \
  bin/wikipedia-make-author

echo "... wikilookup titles"
for S in $( bin/rengu search source '{}' | jq -r .pk ); do
  bin/rengu refresh wikipedia source ${S}
  bin/rengu dump source ${S} | grep -v '^pk:' > tmp/sources/${S}
done

