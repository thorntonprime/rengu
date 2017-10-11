#!/bin/sh

bin/rengu sources verses/* | \
  grep -v null | \
  bin/unicode.py | \
  sed -e 's/^ *//' | sed -e 's/"//g' | sed -e 's/,$//' | sed -e 's/\-/ /g' | \
  sort | uniq -c

