#!/bin/sh
totalfilesize=$(stat -f "%z" "$1")
splitfilesize=$(((totalfilesize/4)/1000000))
megabyte=m
splitfilesizemegabyte=$splitfilesize$megabyte
echo $splitfilesizemegabyte
split -b $splitfilesizemegabyte $1