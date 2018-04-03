#!/bin/bash

SOURCE_PATH=$1
DESTINATION_PATH=$2
if [[ -z $SOURCE_PATH ]] ; then
echo "Please enter source path"
exit 1
elif [[ -z $DESTINATION_PATH ]] ; then 
echo "Please enter destination path"
exit 1
elif ! [ -d $SOURCE_PATH ] ; then
echo "Invalid source path '$SOURCE_PATH'"
exit 1
elif ! [ -d $DESTINATION_PATH ] ; then
echo "Invalid destination path '$DESTINATION_PATH'"
exit 1
elif [[ $SOURCE_PATH -ef $DESTINATION_PATH ]] ; then
echo "Copying denied. Source path '$SOURCE_PATH' is equal to destination path '$DESTINATION_PATH'"
exit 1
fi

read -p "Please, enter max file size (KB): " MAX_SIZE
NUMBER_REGEX='^[0-9]+$'
if ! [[ $MAX_SIZE =~ $NUMBER_REGEX ]] ; then 
echo "Invalid file size: '$MAX_SIZE'"
exit 1
fi

let "MAX_SIZE_BYTES = $MAX_SIZE * 1024"

echo "Searching files greater then $MAX_SIZE KB..."
RESULT_FILES=`find $SOURCE_PATH -type f -size +"$MAX_SIZE_BYTES"c`

if [[ -z $RESULT_FILES ]] ; then
echo "No files greater then $MAX_SIZE_BYTES KB found."
exit 0 
fi
echo "Find files: "
echo "$RESULT_FILES"
echo "Copying to $DESTINATION_PATH."
cp $RESULT_FILES $SOURCE_PATH/. $DESTINATION_PATH >> /dev/null
echo "Copied succesfully."

# find $SOURCE_PATH -type f -size +"$MAX_SIZE_BYTES"c | xargs -I files cp files $SOURCE_PATH/. $DESTINATION_PATH