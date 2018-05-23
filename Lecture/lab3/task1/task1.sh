#!/bin/bash
REGEXP_FILE='./task1/res/regexp.txt'
DATA_FILE='./task1/res/data.txt'
RESULT_FILE='./task1/res/result.txt'

read -r REGEXP < "$REGEXP_FILE"

echo $REGEXP

RESULT=grep -l $REGEXP $DATA_FILE


echo $RESULT