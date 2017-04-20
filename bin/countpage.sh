#!/bin/sh

grep -l "Page: $1" text/* | \
  xargs grep -l "ID: 20c3721c-2af4-449e-a9c0-9791ceb9b9ae" |
  wc -l

