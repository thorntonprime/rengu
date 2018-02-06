#!/bin/sh

bin/rengu people verses/* | \
  grep -v null | \
  sed -e 's/.*://' | \
  tr -d '",:' | \
  sed -e 's/[[:space:]][[:space:]]*/ /g' | \
  sort | uniq | \
  bin/wikipedia > results/people.map

