#!/bin/sh

# AYwH
echo -n "Hafiz "
grep -l 8147df67-439b-4909-bfe3-d55b944af666 verses/* |
  xargs bin/rengu json | jq -r .Source.Locus.Daily | sort -k 1M -k 2g | tail -51 | head -1

# AYwR
echo -n "Rumi  "
grep -l 0a254615-569b-4fb3-96ef-69bd8a224d0d verses/* |
  xargs bin/rengu json | jq -r .Source.Locus.Daily | sort -k 1M -k 2g | tail -8 | head -1

# AYwRilke
echo -n "Rilke "
grep -l 631057a1-0221-4885-ba61-78b661b62b70 verses/* |
  xargs bin/rengu json | jq -r .Source.Locus.Daily | sort -k 1M -k 2g | tail -4 | head -1

# AYwMerton
echo -n "Merton "
grep -l da184f92-f119-42ee-8e45-06ab31cd9624 verses/* |
  xargs bin/rengu json | jq -r .Source.Locus.Daily | sort -k 1M -k 2g | tail -4 | head -1

echo -n "Cloud "
grep -l 937adfe1-da1a-4496-82c5-8061167c097c verses/* |
  xargs bin/rengu json | jq -r '.Source.Locus.Chapter' | \
  grep -v null | \
  msort --line --position 1 --comparison-type numeric --number-system roman --quiet --suppress-log

# Man of Many QUalities
grep -l 503bbcad-73dd-49e6-96a0-bde44020aeb4 verses/* | \
  xargs bin/rengu json | \
  jq -r '@text "\(._id) \(.Hexagram)\t\(if .Locus.Line then .Locus.Line else .Locus.Description end)"' | \
  grep -v null | \
  sort -k 2

grep -l 503bbcad-73dd-49e6-96a0-bde44020aeb4 verses/* | \
  xargs bin/rengu json | \
  jq -r '@text "\(._id) \(.Source.Locus.Hexagram)\t\(if .Source.Locus.Line then .Source.Locus.Line else .Source.Locus.Description end)"' | \
  grep -v null | \
  sort -k 2

# Manhae
grep -l e13d8994-eff6-4830-981a-b30658d44b81 verses/* |
  xargs bin/rengu json | jq -r '._id + " " + (.Source.Locus.Page | tostring)' | sort -k 2g 

