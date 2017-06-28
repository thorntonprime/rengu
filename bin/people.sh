#!/bin/sh

(

bin/rengu verses/* | \
  jq -r .By 2>/dev/null

) | \
  grep -v null | \
  sed -e 's/^ *//' | sed -e 's/"//g' | sed -e 's/,$//' | \
  sort | uniq -c

