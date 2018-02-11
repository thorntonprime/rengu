#!/bin/bash

hafiz() {
  grep -l 8147df67-439b-4909-bfe3-d55b944af666 verses/* |
    xargs bin/rengu json | jq -r .Source.Locus.Daily | sort -k 1M -k 2g | tail -51 | head -1
}

rumi() {
  grep -l 0a254615-569b-4fb3-96ef-69bd8a224d0d verses/* |
    xargs bin/rengu json | jq -r .Source.Locus.Daily | sort -k 1M -k 2g | tail -8 | head -1
}

rilke() {
  grep -l 631057a1-0221-4885-ba61-78b661b62b70 verses/* |
    xargs bin/rengu json | jq -r .Source.Locus.Daily | sort -k 1M -k 2g | tail -4 | head -1
}

merton() {
  grep -l da184f92-f119-42ee-8e45-06ab31cd9624 verses/* |
    xargs bin/rengu json | \
    jq -r .Source.Locus.Daily 2>/dev/null | \
    sort -k 1M -k 2g
}

cloud() {
  grep -l 937adfe1-da1a-4496-82c5-8061167c097c verses/* |
    xargs bin/rengu json | jq -r '.Source.Locus.Chapter' | \
    grep -v null | \
    msort --line --position 1 --comparison-type numeric --number-system roman --quiet --suppress-log
}

iching-siu() {

  (
    grep -l 503bbcad-73dd-49e6-96a0-bde44020aeb4 verses/* | \
      xargs bin/rengu json | \
      jq -r '@text "\(._id) \(.Hexagram)\t\(if .Locus.Line then .Locus.Line else .Locus.Description end)*"'

    grep -l 503bbcad-73dd-49e6-96a0-bde44020aeb4 verses/* | \
      xargs bin/rengu json | \
      jq -r '@text "\(._id) \(.Source.Locus.Hexagram)\t\(if .Source.Locus.Line then .Source.Locus.Line else .Source.Locus.Description end)"'

  ) | grep -v null | sort -k2

}

cold-mountain() {

  grep -l 1ea75c7b-679c-4c20-bf1a-1ea2b09be427 verses/* | \
      xargs bin/rengu json | \
      jq -r '@text "\(._id) \(.Source.Locus.Page)\t\(.Source.Locus.Number)"' | \
      msort --quiet --line -n 2 -c n -n 3 --number-system roman -c n
}

manhae() {
  grep -l e13d8994-eff6-4830-981a-b30658d44b81 verses/* |
    xargs bin/rengu json | \
    jq -r '._id + " " + (.Source.Locus.Number | tostring) + " " + (.Source.Locus.Page | tostring)' | \
    sort -k 2g -k 3g
}

longing() {
  grep -l 82a0aaf9-3f47-4e8c-9075-b14ae205f2a5 verses/* |
    xargs bin/rengu json | jq -r '._id + " " + (.Source.Locus.Page | tostring) + " " + (.Source.Locus.Loc | tostring) + " " + .Title + "/" + .By' | sort -k 2g
}

tosw() {
  grep -l 57c5499b-c3b2-4b09-92a9-a6e977a32050 verses/* | \
    xargs bin/rengu json | \
    jq -r '.Source.Locus.Page' | sort -g | uniq -c
}

FUNS=$( grep '[[:alnum:]]*()' $0 | sed -e 's@() {@@' | paste -sd '|' )

do_help() {
    echo "Select one of:"
    for x in $( echo ${FUNS} | tr '|' ' ' | sed -e 's/FUNS.*//' ); do
      echo "  $x"
    done
}

for ARG in $@; do

  if [[ "$ARG" =~ ^\($FUNS\)$ ]]; then
	$ARG
  elif [[ "$ARG" == "help" ]]; then
	do_help
  else
    echo "Not found (try help)"
  fi

done

