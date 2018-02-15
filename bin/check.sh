#!/bin/sh

(
  bin/rengu search verse '{}' | \
    jq -r .pk | \
    xargs bin/rengu-extract-authors verse

  bin/rengu search source '{}' | \
    jq -r .pk | \
    xargs bin/rengu-extract-authors source
) | \
  sort | uniq | \
  bin/rengu-check-author > output/author.check

