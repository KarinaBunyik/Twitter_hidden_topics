#!/bin/sh
# ex. ./run_twitter_mallet.sh malletTwitterLDAJuneAll output_LDA_june_all.mallet swedish_stoplist.txt topic-keys-LDA-june-all.txt
cd /Users/karinabunyik/mallet-2.0.7
./bin/mallet import-dir \
	--input $1 \
	--output $2 \
	--keep-sequence  \
	--remove-stopwords \
	--extra-stopwords $3 \
	--token-regex '[\p{L}\p{M}]+' \
	--skip-html 
	#--gram-sizes 1,2 \
	#--keep-sequence-bigrams
./bin/mallet train-topics \
	--input $internaldir$2 \
	--inferencer-filename $9 \
	--evaluator-filename ${11} \
	--num-topics $6 \
	--num-top-words $7 \
	--num-iterations $8 \
	--doc-topics-threshold 0.1 \
	--output-topic-keys $4 \
	--output-doc-topics $5 \
	--num-threads 8 
	#--use-ngrams true 
	#--xml-topic-report topic-report.xml
./bin/mallet infer-topics \
  --input $internaldir$2 \
  --inferencer $9 \
  --output-doc-topics ${10} \
  --num-iterations $8
./bin/mallet evaluate-topics \
  --evaluator ${11} \
  --input $2 \
  --output-doc-probs ${12} \
  --output-prob ${13}

