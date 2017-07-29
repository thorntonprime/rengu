#!/bin/sh

# AYwH
grep -l 8147df67-439b-4909-bfe3-d55b944af666 verses/* |
  xargs ls -t 2>/dev/null | head -1 | \
  xargs -n1 -i yaml r {} Description

# AYwR
grep -l 0a254615-569b-4fb3-96ef-69bd8a224d0d verses/* |
  xargs ls -t 2>/dev/null | head -1 | \
  xargs -n1 -i yaml r {} Description

# AYwRilke
grep -l 631057a1-0221-4885-ba61-78b661b62b70 verses/* |
  xargs ls -t 2>/dev/null | head -1 | \
  xargs -n1 -i yaml r {} Description

