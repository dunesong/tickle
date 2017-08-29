#!/usr/bin/env bash

TEST='test 0: should echo non-tickle commands without modification'

results=$(../tickle.py -e data/test.0.dat | diff - data/test.0.dat)

if [ "$results" ]; then
  echo "$TEST ... failed"
  exit 1
else
  echo "$TEST ... passed"
fi
