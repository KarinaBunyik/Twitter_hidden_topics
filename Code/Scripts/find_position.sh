#!/bin/sh
awk -v find=5746 '{ printf ("%s", index($0,find) ) }' $1
