#!/bin/sh
START=$(date +%s)
totallinenumber=$(sed -n '$=' $1)
echo $totallinenumber
linenumber=$(((totallinenumber/4)+5))
echo $linenumber
split -l $linenumber $1 "/Users/karinabunyik/BTSync/Data/"
END=$(date +%s)
DIFF=$(( $END - $START ))
echo "It took $DIFF seconds"