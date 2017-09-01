#!/usr/bin/env bash

TEST="test 2: should create temporary copy and preserve file permissions when --merge option is used"
TEST_DATA_ORIG=data/test.2.dat
TEST_DATA=data/test.2.tmp

cp "$TEST_DATA_ORIG" "$TEST_DATA"

orig_perm=$(stat -c %a "$TEST_DATA")
results=$(../tickle.py -m "$TEST_DATA")
new_perm=$(stat -c %a "$TEST_DATA")

rm "$TEST_DATA"

if [ "$orig_perm" != "$new_perm" ]; then
  echo "$TEST ... permissions differ, failed"
  exit 1
else
  echo "$TEST ... passed"
fi
