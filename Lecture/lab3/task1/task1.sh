#!/bin/bash
REGEXP_FILE='./task1/res/regexp.txt'
DATA_FILE='./task1/res/data.txt'
RESULT_FILE='./task1/res/result.txt'

read -r REGEXP < $REGEXP_FILE
read -r DATA < $DATA_FILE
echo $REGEXP
echo "Data: $DATA"

# echo $(grep -E -o "$REGEXP" $DATA_FILE)
grep -E -o "$REGEXP" $DATA_FILE >> $RESULT_FILE
