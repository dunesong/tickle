#!/usr/bin/env bash

TEST_NAME='test 2'
TEST="$TEST_NAME: should create temporary copy and preserve file permissions when --merge option is used"
TEST_DATA_ORIG=data/test.2.dat
TEST_DATA=data/test.2.tmp

cp "$TEST_DATA_ORIG" "$TEST_DATA"

orig_perm=$(stat -c %a "$TEST_DATA")
orig_birth=$(stat -c %w "$TEST_DATA")
orig_access=$(stat -c %x "$TEST_DATA")
orig_modify=$(stat -c %y "$TEST_DATA")
orig_change=$(stat -c %z "$TEST_DATA")

results=$(../tickle.py -m data/test.2.dat)

new_perm=$(stat -c %a "$TEST_DATA")
new_birth=$(stat -c %w "$TEST_DATA")
new_access=$(stat -c %x "$TEST_DATA")
new_modify=$(stat -c %y "$TEST_DATA")
new_change=$(stat -c %z "$TEST_DATA")

rm "$TEST_DATA"

echo "$TEST"

if [ "$orig_birth" != "$new_birth" ]; then
  echo "$TEST_NAME ... birth datetimes differ, warning"
fi
if [ "$orig_access" != "$new_access" ]; then
  echo "$TEST_NAME ... access datetimes differ, warning"
fi
if [ "$orig_modify" != "$new_modify" ]; then
  echo "$TEST_NAME ... modify datetimes differ, warning"
fi
if [ "$orig_change" != "$new_change" ]; then
  echo "$TEST_NAME ... change datetimes differ, warning"
fi
if [ "$orig_perm" != "$new_perm" ]; then
  echo "$TEST_NAME ... permissions differ, failed"
  exit 1
else
  echo "$TEST_NAME ... passed"
fi
