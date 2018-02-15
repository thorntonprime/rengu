#!/bin/sh

cat output/author.check | grep 'NO MATCH' | \
  cut -d'!' -f 1 | tr -d "'" | xargs -n1 -i bin/rengu fuzz author "{}" | \
  tee output/author.fix

cat output/author.check | grep 'NO MATCH' | \
  cut -d'!' -f 1 | tr -d "'" | \
  bin/wikipedia-make


