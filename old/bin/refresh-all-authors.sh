#!/bin/sh

for A in $( bin/rengu search author '{}' | jq -r .pk ); do

  bin/rengu refresh wikipedia author ${A}
  bin/rengu dump author ${A} | grep -v '^pk:' > tmp/authors/${A}

done
