#!/bin/sh

# Pre-Checks
echo "Running Pre-Checks"
yamllint -f parsable verses/* authors/* sources/* | tee check/yaml.check

# Clear and Load Data
echo "Clearing and loading data"
rm -rf db
bin/rengu load verse verses/* > check/verses.load
bin/rengu load source sources/* > check/sources.load
bin/rengu load author authors/* > check/authors.load

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
  sort | uniq -c | tee check/authors.list | \
  cut -c9- | \
  bin/rengu-exists-author > check/authors.exists


echo " ... verse author extract"
bin/rengu search verse '{}' | \
  jq -r .pk | \
  xargs bin/rengu extract author > check/verse-author.extract

echo " ... missing authors counts"
grep "NOT_FOUND" check/verse-author.extract | \
  cut -c88- | sort | uniq -c | sort -g > check/missing-authors.count

echo " ... verse source extract"
bin/rengu search verse '{}' |  \
  jq -r .pk | \
  xargs bin/rengu extract source > check/verse-sources.extract

echo " ... titles extract"
bin/rengu search verse '{}' | \
  jq -r .pk | \
  xargs bin/rengu-extract-title | \
  sort | uniq -c | sort -g > check/titles.list

echo " ... fuzz authors"
cat check/missing-authors.count | \
  cut -c9- | \
  bin/rengu-fuzz-author > check/authors.fuzz

echo " ... exists titles"
cat check/titles.list | cut -c9- | \
  bin/rengu-exists-source  > check/titles.exists

echo " ... title reference count"
( grep 'NO MATCH' check/titles.exists | \
  cut -d '!' -f 1 | \
  while read A ; do C=$( grep -l "Title: ${A}$" verses/* | wc -l); \
  printf "$C\t $A\n"; read A; done | \
  sort -k1 -g -k2 ) > check/titles.count

echo " ... fuzz titles"
cat check/titles.exists | grep 'NO MATCH' | \
  cut -d'!' -f 1 | \
  bin/rengu-fuzz-title > check/titles.fuzz

echo " ... fix verses"
bin/rengu search verse '{}' | jq -r .pk | \
  xargs bin/rengu-fix-verse > check/verses.fix

echo " ... tag check authors"
cat authors/* | \
  grep '^ *[[:alnum:]]*:' | cut -d: -f1 | awk '{ print $1 }' | sort | uniq \
  > check/authors.tags

echo " ... tag check sources"
cat sources/* | \
  grep '^ *[[:alnum:]]*:' | cut -d: -f1 | awk '{ print $1 }' | sort | uniq \
  > check/sources.tags

echo " ... tag check verses"
cat verses/* | \
  grep '^ *[[:alnum:]]*:' | cut -d: -f1 | awk '{ print $1 }' | sort | uniq \
  > check/verses.tags

exit
############################ END

# Fix-Ups
echo " ... wikilookup authors"
cat check/missing-authors.count | cut -c9- | \
  bin/wikipedia-make-author

echo "... wikilookup titles"
for S in $( bin/rengu search source '{}' | jq -r .pk ); do
  bin/rengu refresh wikipedia source ${S}
  bin/rengu dump source ${S} | grep -v '^pk:' > tmp/sources/${S}
done

