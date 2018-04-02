#!/bin/bash

SEARCH_PATH=$1
SUFFIX=$2

if [[ -z $SEARCH_PATH ]]
then
echo "Please enter search path"
exit 1
elif [[ -z $SUFFIX ]]
then 
echo "Please enter search suffix"
exit 1
elif ! [ -d $SEARCH_PATH ]
then
echo "Invalid search path '$SEARCH_PATH'"
exit 1
else
echo "Searching file with suffix '$SUFFIX' in $SEARCH_PATH directory..."
fi

SEARCH_RESULT=`find $SEARCH_PATH -name "*$SUFFIX" -type f -printf "%s %p\n" | sort -n | cut -d " " -f 2-`
echo "Search result: $SEARCH_RESULT"
read -p "Please enter destination filename: " DESTINATION
echo "$SEARCH_RESULT">"$DESTINATION"