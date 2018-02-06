#!/bin/sh

bin/rengu sources verses/* | \
  grep -v null | \
  sed -e 's/^ *//' | sed -e 's/"//g' | sed -e 's/,$//' | sed -e 's/\-/ /g' | \
  sort | uniq | \
  bin/wikipedia > results/title.map

