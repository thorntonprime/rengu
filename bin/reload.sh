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

# Author checks

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

echo " ... fuzz authors"
cat check/missing-authors.count | \
  cut -c9- | \
  bin/rengu-fuzz-author > check/authors.fuzz

echo " ... map authors to proper names"
cut -c88- check/verse-author.extract | \
  sort | uniq > maps/proper-people.txt

echo " ... tag check authors"
cat authors/* | \
  grep '^ *[[:alnum:]]*:' | cut -d: -f1 | awk '{ print $1 }' | sort | uniq \
  > check/authors.tags

# Titles
echo " ... verse source extract"
bin/rengu search verse '{}' |  \
  jq -r .pk | \
  xargs bin/rengu extract source > check/verse-sources.extract

echo " ... count missing titles"
grep NO_MATCH check/verse-sources.extract | \
  cut -c75- | cut -d/ -f1 | \
  sort | uniq -c | sort -g > check/missing-titles.count

echo " ... fuzz titles"
cut -c9- check/missing-titles.count | \
  bin/rengu-fuzz-title > check/titles.fuzz

echo " ... tag check sources"
cat sources/* | \
  grep '^ *[[:alnum:]]*:' | cut -d: -f1 | awk '{ print $1 }' | sort | uniq \
  > check/sources.tags

# Verses
echo " ... extract words"
bin/rengu search verse '{}' | jq -r .pk | \
  xargs bin/rengu extract words | cut -c38- | \
  sort | uniq -c | sort -g > maps/words.count

cut -c9- maps/words.count | bin/spellcheck | \
  grep False | cut -c7- | sort | uniq > check/words.misspell

echo " ... fix verses"
bin/rengu search verse '{}' | jq -r .pk | \
  xargs bin/rengu-fix-verse > check/verses.fix

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

