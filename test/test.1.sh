#!/usr/bin/env bash

TEST='test 1: should run through multiple tickler files'

results=$(../tickle.py data/test.1.0.dat data/test.1.1.dat | diff - data/test.1.results.dat)

if [ "$results" ]; then
  echo "$TEST ... failed"
  exit 1
else
  echo "$TEST ... passed"
fi
