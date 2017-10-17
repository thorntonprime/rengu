#!/bin/sh

# AYwH
echo -n "Hafiz "
grep -l 8147df67-439b-4909-bfe3-d55b944af666 verses/* |
  xargs bin/rengu json | jq -r .Source.Locus.Daily | sort -k 1M -k 2g | tail -51 | head -1

# AYwR
echo -n "Rumi  "
grep -l 0a254615-569b-4fb3-96ef-69bd8a224d0d verses/* |
  xargs bin/rengu json | jq -r .Source.Locus.Daily | sort -k 1M -k 2g | tail -9 | head -1

# AYwRilke
echo -n "Rilke "
grep -l 631057a1-0221-4885-ba61-78b661b62b70 verses/* |
  xargs bin/rengu json | jq -r .Source.Locus.Daily | sort -k 1M -k 2g | tail -4 | head -1

