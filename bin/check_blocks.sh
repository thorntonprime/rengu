#!/bin/sh

# Find all text with more than 2 blocks

for x in text/*; do
  echo "$( grep '^---' $x | wc -l)  $x"
done | \
awk ' ( $1 > 2 )'

