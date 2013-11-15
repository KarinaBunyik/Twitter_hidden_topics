#!/bin/sh
cd /Users/karinabunyik/mallet-2.0.7
inputdir='/Users/karinabunyik/BTSync/Twitter_hidden_topics/Code/Internal_data/'
internaldir='/Users/karinabunyik/BTSync/Twitter_hidden_topics/Code/Internal_data/'
outdir='/Users/karinabunyik/BTSync/Twitter_hidden_topics/Output/'
./bin/mallet import-dir --input $inputdir$1 --output $internaldir$2 --keep-sequence --remove-stopwords --extra-stopwords $internaldir$3 --token-regex '[\p{L}\p{M}]+' --skip-html
#/Users/karinabunyik/BTSync/Twitter_hidden_topics/Code/Internal_data/malletTwitterOctober
#/Users/karinabunyik/BTSync/Twitter_hidden_topics/Code/Internal_data/output.mallet
#/Users/karinabunyik/BTSync/Twitter_hidden_topics/Code/Internal_data/swedish_stoplist.txt
#/Users/karinabunyik/BTSync/Twitter_hidden_topics/Output/topic-state.gz
./bin/mallet train-topics --input $internaldir$2 --num-topics 20 --output-topic-keys $outdir$4
#./bin/mallet train-topics --input $internaldir$2 --num-topics 10 --output-doc-topics $4
# /Users/karinabunyik/BTSync/Twitter_hidden_topics/Code/Internal_data/malletTwitterOctober /Users/karinabunyik/BTSync/Twitter_hidden_topics/Code/Internal_data/output.mallet /Users/karinabunyik/BTSync/Twitter_hidden_topics/Code/Internal_data/swedish_stoplist.txt /Users/karinabunyik/BTSync/Twitter_hidden_topics/Output/topic-state.gz