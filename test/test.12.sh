#!/usr/bin/env bash

TEST_NAME="test 12: should recognize 'yesterday' as a valid tickle date"
TODAY=$(date --iso-8601=date)
YESTERDAY=$(date --iso-8601=date -d "-1 day")
TEST_DATA="#tickle on $YESTERDAY say Success\n#tickle on $TODAY say Failure"

results=$(echo -e "$TEST_DATA" | ../tickle.py --date yesterday -)

if [ "$results" != "Success" ]; then
  echo "$TEST_NAME ... failed"
  exit 1
else
  echo "$TEST_NAME ... passed"
fi
