#!/bin/bash

# if ./task1/task1.sh # Test fail on no args
# then
# echo 'ERROR: Script successed with no args'
# exit 1
# elif ./task1/task1.sh ./task1/test/test_files
# then 
# echo 'ERROR: Script successed with no search suffix'
# exit 1
# elif [ ./task1/task1.sh __INVALID_DIRECTORY__ suffix ]
# then
# echo 'ERROR: Script succesed with invalid search directory'
# exit 1
# fi

RESULT_FILE='result.data'

echo $RESULT_FILE | ./task1/task1.sh ./task1/test/test_files .test 
echo "Executed successed. Check result in $RESULT_FILE"