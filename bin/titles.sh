#!/bin/sh

(

bin/rengu verses/* | \
  jq -r .Source.Title 2>/dev/null

bin/rengu verses/* | \
  jq -r .Source.Source.Title 2>/dev/null

) | \
  grep -v null | \
  bin/unicode.py | \
  sed -e 's/^ *//' | sed -e 's/"//g' | sed -e 's/,$//' | sed -e 's/\-/ /g' | \
  sort | uniq -c

