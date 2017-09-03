#!/usr/bin/env bash

TEST='test 4: should read from STDIN'

results1=$(cat data/test.4.dat | ../tickle.py - | diff - data/test.4.results.dat)
results2=$(cat data/test.4.dat | ../tickle.py | diff - data/test.4.results.dat)

if [ "$results1" ] || [ "$results2" ]; then
  echo "$TEST ... failed"
  exit 1
else
  echo "$TEST ... passed"
fi
