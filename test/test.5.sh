#!/usr/bin/env bash

TEST_NAME="test 5: should merge tickles into source file with --merge option"
TEST_DATA_ORIG=data/test.5.dat
TEST_DATA=data/test.5.tmp

cp "$TEST_DATA_ORIG" "$TEST_DATA"

../tickle.py -m "$TEST_DATA"
results=$(diff "$TEST_DATA" data/test.5.results.dat)

rm "$TEST_DATA"

if [ "$results" ]; then
  echo "$TEST_NAME ... failed"
  exit 1
else
  echo "$TEST_NAME ... passed"
fi
