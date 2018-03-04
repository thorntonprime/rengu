#!/bin/sh

bin/rengu search verse '{}' | \
  jq -r .pk | \
  xargs bin/rengu classify train

