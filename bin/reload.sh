#!/bin/sh

# Pre-Checks
echo "Running Pre-Checks"
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

  bin/rengu search author '{}' | \
    jq -r .Members[]? 
) | \
  sort | uniq -c | tee output/authors.list | \
  cut -c9- | \
  bin/rengu-exists-author > output/authors.exists


echo " ... author reference count"
( grep 'NO MATCH' output/authors.exists | \
  cut -d '!' -f 1 | \
  while read A ; do C=$( grep -l "$A" verses/* | wc -l); \
  printf "$C\t $A\n"; read A; done | \
  sort -k1 -g -k2 ) > output/authors.count

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

echo " ... title reference count"
( grep 'NO MATCH' output/titles.exists | \
  cut -d '!' -f 1 | \
  while read A ; do C=$( grep -l "Title: ${A}$" verses/* | wc -l); \
  printf "$C\t $A\n"; read A; done | \
  sort -k1 -g -k2 ) > output/titles.count

echo " ... fuzz titles"
cat output/titles.exists | grep 'NO MATCH' | \
  cut -d'!' -f 1 | \
  bin/rengu-fuzz-title > output/titles.fuzz

echo " ... fix verses"
bin/rengu search verse '{}' | jq -r .pk | \
  xargs bin/rengu-fix-verse > output/verses.fix

echo " ... tag check authors"
cat authors/* | \
  grep '^ *[[:alnum:]]*:' | cut -d: -f1 | awk '{ print $1 }' | sort | uniq \
  > output/authors.tags

echo " ... tag check sources"
cat sources/* | \
  grep '^ *[[:alnum:]]*:' | cut -d: -f1 | awk '{ print $1 }' | sort | uniq \
  > output/sources.tags

echo " ... tag check verses"
cat verses/* | \
  grep '^ *[[:alnum:]]*:' | cut -d: -f1 | awk '{ print $1 }' | sort | uniq \
  > output/verses.tags

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

