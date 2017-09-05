#!/usr/bin/env bash

TEST_NAME="test 8: should recognize 'today' as a valid tickle date"
DATE="1066-10-14"
TODAY=$(date --iso-8601=date)
TEST_DATA="#tickle on $TODAY say Success\n#tickle on $DATE say Failure"

results=$(echo -e "$TEST_DATA" | ../tickle.py --date today -)

if [ "$results" != "Success" ]; then
  echo "$TEST_NAME ... failed"
  exit 1
else
  echo "$TEST_NAME ... passed"
fi
