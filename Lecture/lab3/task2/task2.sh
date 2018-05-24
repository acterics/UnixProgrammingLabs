#!/bin/bash


DATA_FILE='./task2/res/data.txt'
RESULT_FILE='./task2/res/result.txt'

sed -E 's/(^[0-9]{4})\/(1[0-2]{1})\/([1-2]{1}[0-9]{1}|3[0-1]$)/\3.\2.\1/g' $DATA_FILE > $RESULT_FILE
sed -i -E 's/(^[0-9]{4})\/([1-9]{1})\/([1-2]{1}[0-9]{1}|3[0-1]$)/\3.0\2.\1/g' $RESULT_FILE
sed -i -E 's/(^[0-9]{4})\/([1-9]{1})\/([1-9]{1}$)/0\3.0\2.\1/g' $RESULT_FILE
sed -i -E 's/(^[0-9]{4})\/(1[0-2]{1})\/([1-9]{1}$)/0\3.\2.\1/g' $RESULT_FILE