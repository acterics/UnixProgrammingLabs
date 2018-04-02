#!/bin/bash

SOURCE_PATH=$1
DESTINATION_PATH=$2
if [[ -z $SOURCE_PATH ]]
then
echo "Please enter source path"
exit 1
elif [[ -z $DESTINATION_PATH ]]
then 
echo "Please enter destination path"
exit 1
elif ! [ -d $SOURCE_PATH ]
then
echo "Invalid source path '$SOURCE_PATH'"
exit 1
elif ! [ -d $DESTINATION_PATH ]
then
echo "Invalid destination path '$DESTINATION_PATH'"
exit 1
fi

# cd -P "$DESTINATION_PATH"
# REAL_DESTINATION_PATH=`pwd`
# cd -P "$SOURCE_PATH"
# REAL_SOURCE_PATH=`pwd`

# echo $REAL_SOURCE_PATH
# echo $REAL_DESTINATION_PATH

# if [[ $REAL_SOURCE_PATH == $REAL_DESTINATION_PATH ]]
# then
# echo "Copying denied. Source path '$SOURCE_PATH' is equal to destination path '$DESTINATION_PATH'"
# exit 1
# fi

read -p "Please, enter max file size (KB): " MAX_SIZE
let "MAX_SIZE_BYTES = $MAX_SIZE * 10"

# echo $MAX_SIZE_BYTES
# cp -R $SOURCE_PATH/. $DESTINATION_PATH
# echo `let 1024 * $MAX_SIZE`
find $SOURCE_PATH -type f -size +$MAX_SIZE_BYTES