#!/bin/sh

cat | \
  sed -e 's/\. \([a-z]\)/, \1/g' | \
  sed -e 's/\. *\. *\. *\. */. ... /g' | sed -e 's/…/ .../g' | \
  sed -e 's/\([a-z]\)—  */\1 -- /g' | sed -e 's/ *—$/ --/' | \
  sed -e 's/:/：/g'

