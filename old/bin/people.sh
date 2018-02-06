#!/bin/sh

bin/rengu people verses/* | \
  grep -v null | \
  sed -e 's/.*://' | \
  tr -d '",:' | \
  bin/unicode.py | \
  sed -e 's/[[:space:]][[:space:]]*/ /g' | \
  sort | uniq -c

