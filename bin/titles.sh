#!/bin/sh

bin/rengu verses/* | \
  jq -r .Source.Source.Title 2>/dev/null | \
  grep -v null | \
  sed -e 's/^ *//' | \
  sort | uniq
