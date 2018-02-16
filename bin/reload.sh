#!/bin/sh

# Pre-Checks
yamllint -f parsable verses/* authors/* sources/*

# Clear and Load Data
rm -rf db
bin/rengu load verse verses/*
bin/rengu load source sources/*
bin/rengu load author authors/*

# Post-Checks
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

bin/rengu search verse '{}' | \
  jq -r .pk | \
  xargs bin/rengu-extract-source | \
  sort | uniq -c | sort -g > output/titles.list

cat output/author.check | grep 'NO MATCH' | \
  cut -d'!' -f 1 | \
  bin/rengu-fuzz-author > output/author.fuzz

# Fix-Ups
cat output/author.check | grep 'NO MATCH' | \
  cut -d'!' -f 1 | tr -d "'" | \
  bin/wikipedia-make

