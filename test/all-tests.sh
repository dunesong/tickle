#!/usr/bin/env bash

declare -i test_count=0
declare -i failure_count=0

for i in test.*.sh; do
  "./$i"
  test_status=$?

  test_count+=1
  if (( "$test_status" != 0 )) ; then
    failure_count+=1
  fi
done

echo ''
if (( "$failure_count" > 0 )) ; then
  echo "$failure_count/$test_count tests failed"
else
  echo "$test_count tests passed"
fi
