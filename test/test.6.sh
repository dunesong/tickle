#!/usr/bin/env bash

TEST_NAME="test 6: should tickle 'on <date>' when tickle date is today"
DATE=$(date --iso-8601=date)

results=$(echo "# tickle on $DATE say Success" | ../tickle.py -)

if [ "$results" != "Success" ]; then
  echo "$TEST_NAME ... failed"
  exit 1
else
  echo "$TEST_NAME ... passed"
fi
