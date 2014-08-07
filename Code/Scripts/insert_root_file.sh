#!/bin/sh
cat $2 $1 $3 > temp.xml
mv temp.xml $1
