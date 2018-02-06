#!/bin/sh

grep NOMATCH output/check.out | \
  sed -e 's/.*NOMATCH //' | \
  sort | uniq -c | sort -g
