#!/bin/sh

for f in GenRoot/pp*; do
    echo "Processing " $f
    ./analysis $f root/`basename $f`
done
