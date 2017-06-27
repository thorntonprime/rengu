#!/bin/sh

grep ':' verses/* | \
  awk -F: '{ print $2 }' | \
  sed -e 's/\([- ]\)*//' | \
  sort | \
  uniq

