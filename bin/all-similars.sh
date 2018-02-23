#!/bin/sh

for V in $( bin/rengu search verse '{}' | jq -r .pk ); do

    VSHORT=$( echo $V | cut -c1-4 )
    [ -d tmp/similars/${VSHORT} ] || mkdir -p tmp/similars/${VSHORT}

    for Y in $( bin/rengu search verse "{ 'pk' : { '\$gt' : '${V}' } }" | jq -r .pk ); do

	ts bin/rengu similar verse ${V} ${Y} > tmp/similars/${VSHORT}/${V}-${Y}

    done

done
