#!/bin/sh

for V in $( bin/rengu search verse '{}' | jq -r .pk ); do

    echo ${V}
    ts -n bin/similar-one.sh ${V}

done
