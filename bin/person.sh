#!/bin/sh

SHOWUUID=0

if [ "$1" == "-u" ]; then
  SHOWUUID=1
  shift
fi

for PERSON in "$@"; do

  PUID=""

  for pdata in people/*; do
    yaml r ${pdata} | grep -qi "${PERSON}" && PUID=$( basename ${pdata} )
    if [ "${PUID}" != "" ]; then
      break
    fi
  done

  if [ "${PUID}" == "" ]; then
    break
  fi

  grep -l ${PUID} verses/* |
    xargs bin/rengu json | jq -r '._id + "|" + .Source.Locus.Daily + "|" + .Title'

done
 
