#!/usr/bin/env bash

TEST_NAME="test 11: should recognize 'overmorrow' as a valid tickle date"
TODAY=$(date --iso-8601=date)
OVERMORROW=$(date --iso-8601=date -d "+2 days")
TEST_DATA="#tickle on $OVERMORROW say Success\n#tickle on $TODAY say Failure"

results=$(echo -e "$TEST_DATA" | ../tickle.py --date overmorrow -)

if [ "$results" != "Success" ]; then
  echo "$TEST_NAME ... failed"
  exit 1
else
  echo "$TEST_NAME ... passed"
fi
