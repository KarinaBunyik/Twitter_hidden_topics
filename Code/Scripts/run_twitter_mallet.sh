#!/bin/sh
# ex. ./run_twitter_mallet.sh malletTwitterLDAJuneAll output_LDA_june_all.mallet swedish_stoplist.txt topic-keys-LDA-june-all.txt
cd /Users/karinabunyik/mallet-2.0.7
./bin/mallet import-dir \
	--input $1 \
	--output $2 \
	--keep-sequence true \
	--remove-stopwords true\
	--extra-stopwords $3 \
	--token-regex '[\p{L}\p{M}]+' \
	#--encoding UTF-8 \
	--gram-sizes 2 \
	--keep-sequence-bigrams true
./bin/mallet split \
	--input $2 \
	--training-file ${14} \
	--testing-file ${15} \
	--training-portion .8
./bin/mallet train-topics \
	--input ${14} \
	--inferencer-filename $9 \
	--evaluator-filename ${11} \
	--num-topics $6 \
	--num-top-words $7 \
	--num-iterations $8 \
	#--use-ngrams true \
	--doc-topics-threshold 0.1 \
	--output-topic-keys $4 \
	--output-doc-topics $5 \
	--num-threads 8 
./bin/mallet infer-topics \
  --input $internaldir$2 \
  --inferencer $9 \
  --output-doc-topics ${10} \
  --num-iterations $8
./bin/mallet evaluate-topics \
  --evaluator ${11} \
  --input ${15} \
  --output-doc-probs ${13} \
  --output-prob ${12}

  ./bin/mallet run cc.mallet.util.DocumentLengths --input ${15} > ttt.txt

