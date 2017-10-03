#!/bin/sh

(

bin/rengu verses/* | \
  jq -r .By 2>/dev/null

) | \
  grep -v null | \
  sed -e 's/.*://' | \
  tr -d '",:' | \
  bin/unicode.py | \
  sed -e 's/[[:space:]][[:space:]]*/ /g' | \
  sort | uniq -c

