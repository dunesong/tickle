#!/usr/bin/env bash

TEST_NAME="test 13: should recognize 'ereyesterday' as a valid tickle date"
TODAY=$(date --iso-8601=date)
EREYESTERDAY=$(date --iso-8601=date -d "-2 days")
TEST_DATA="#tickle on $EREYESTERDAY say Success\n#tickle on $TODAY say Failure"

results=$(echo -e "$TEST_DATA" | ../tickle.py --date ereyesterday -)

if [ "$results" != "Success" ]; then
  echo "$TEST_NAME ... failed"
  exit 1
else
  echo "$TEST_NAME ... passed"
fi
