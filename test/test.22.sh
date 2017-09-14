#!/usr/bin/env bash
#
# 4-sigma = 99.993666%
# http://stattrek.com/online-calculator/binomial.aspx

printf "test 22: should be able to tickle randomly (using statistical tests, failure if results are outside of 4-sigma) ... " 

DEBUG=false
while getopts ':d' opt; do
    case $opt in
    d)
        DEBUG=true
        ;;
    \?)
        echo "Invalid option: -$OPTARG" >&2
        ;;
    esac
done

results=$(echo "#tickle randomly interval 1 say Success" | ../tickle.py 2>&1)

if [ "$DEBUG" == true ]; then
    echo "$results"
fi

if [ "$results" != "Success" ]; then
    echo "failed"
    exit 1
fi

trials_passed=0
for i in $(seq 1 48); do
    results=$(echo "#tickle randomly interval 2 say Success" | ../tickle.py 2>&1)

    if [ "$DEBUG" == true ]; then
        echo "$results"
    fi

    if [ "$results" == "Success" ]; then
        trials_passed=$((trials_passed +1))
    fi
done

if [ "$trials_passed" -lt 9 ] || [ "$trials_passed" -gt 41 ]; then
  echo "failed"
  exit 1
else
  echo "passed"
fi
