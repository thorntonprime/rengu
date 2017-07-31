#!/bin/sh

bin/rengu verses/* | jq -r .Tags | tr -d '][",' | grep -v null | sort | uniq

