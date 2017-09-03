#!/usr/bin/env bash

TEST_NAME="test 7: should tickle 'on <date>' when tickle date is specified"
DATE="1066-10-14"
TODAY=$(date --iso-8601=date)
TEST_DATA="#tickle on $DATE say Success\n#tickle on $TODAY say Failure"

results=$(echo -e "$TEST_DATA" | ../tickle.py --date "$DATE" -)

if [ "$results" != "Success" ]; then
  echo "$TEST_NAME ... failed"
  exit 1
else
  echo "$TEST_NAME ... passed"
fi
