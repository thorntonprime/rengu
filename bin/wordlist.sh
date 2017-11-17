#!/bin/sh

bin/rengu json verses/* | jq -r .Body | \
  tr -d '".,!?:;-' | tr -d "'" | \
  xargs -n1 echo | \
  sort | uniq -c | sort -g \
  > results/words.txt

