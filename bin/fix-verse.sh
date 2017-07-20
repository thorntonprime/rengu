#!/bin/sh

cat | \
  sed -e 's/  */ /g' | \
  sed -e 's/\([a-z]\)\.  *\([a-z]\)/\1, \2/g' | \
  sed -e 's/  *\. *\. *\. */ ... /g' | \
  sed -e 's/…/ .../g' | \
  sed -e 's/\([,;:\.]\) *\. *\. *\. */\1 ... /g' | \
  sed -e 's/\([A-Za-z\.,;:-]\)  *\([A-Za-z-]\)/\1 \2/g' | \
  sed -e 's/\([a-z]\)—  */\1 -- /g' | \
  sed -e 's/ *—$/ --/g' | \
  sed -e 's/  *o  *f  */ of /g' | \
  sed -e 's/:/：/g' | \
  sed -e 's/[——-]/-/g' | \
  sed -e 's/ *$//g' | \
  cat
