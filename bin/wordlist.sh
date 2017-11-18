#!/bin/sh

bin/rengu json verses/* | jq -r .Body | \
  tr -d '".,!?:;-' | tr -d "'" | \
  xargs -n1 echo | \
  tr 'A-Z' 'a-z' | \
  bin/unicode.py | \
  sort | uniq -c | sort -g \
  > results/words.txt

