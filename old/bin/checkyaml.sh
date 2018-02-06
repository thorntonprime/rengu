#!/bin/sh

for F in $@; do

  yaml r ${F} | \
  grep ':' | \
  awk -F: '{ print $1 }' | \
  sed -e 's/^\([- ]\)*//'

done | sort | uniq

