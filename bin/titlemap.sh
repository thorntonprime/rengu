#!/bin/sh

bin/rengu wikisources verses/* | \
  sort | uniq \
  > results/titlemap.txt
