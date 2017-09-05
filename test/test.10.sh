#!/usr/bin/env bash

TEST_NAME="test 8: should recognize 'tomorrow' as a valid tickle date"
TODAY=$(date --iso-8601=date)
TOMORROW=$(date --iso-8601=date -d "+1 day")
TEST_DATA="#tickle on $TOMORROW say Success\n#tickle on $TODAY say Failure"

results=$(echo -e "$TEST_DATA" | ../tickle.py --date tomorrow -)

if [ "$results" != "Success" ]; then
  echo "$TEST_NAME ... failed"
  exit 1
else
  echo "$TEST_NAME ... passed"
fi
