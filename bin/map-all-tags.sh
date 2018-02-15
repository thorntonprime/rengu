#!/bin/sh

bin/rengu search verse '{}' | \
  jq -r .Tags[]? | tr '=' '\n' | \
  sort | uniq -c
