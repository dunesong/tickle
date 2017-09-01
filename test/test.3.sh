#!/usr/bin/env bash

TEST='test 3: should run daily tickles'

results=$(../tickle.py data/test.3.dat | diff - data/test.3.results.dat)

if [ "$results" ]; then
  echo "$TEST ... failed"
  exit 1
else
  echo "$TEST ... passed"
fi
