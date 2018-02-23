#!/bin/sh

V=$1
VSHORT=$( echo $V | cut -c1-4 )

[ -d tmp/similars/${VSHORT} ] || mkdir -p tmp/similars/${VSHORT}

bin/rengu similar verse ${V} \
	$( bin/rengu search verse "{ 'pk' : { '\$gt' : '${V}' } }" | jq -r .pk ) | \
	> tmp/similars/${VSHORT}/${V}

