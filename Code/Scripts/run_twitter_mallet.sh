#!/bin/sh
cd /Users/karinabunyik/mallet-2.0.7
./bin/mallet import-dir --input $1 --output $2 --keep-sequence --remove-stopwords
