#!/usr/bin/env bash

TEST_NAME="test 14: should be able to tickle weekly"

EXPECTED_RESULTS=$(cat <<'EOF'
Success
Success
Success
Success
Success
Success
Success
Success
EOF
)

results=$(../tickle.py --date '1970-01-01' 2>&1 <<'EOF'
# tickle weekly mon, tue, wed, thu, fri, sat, sun say Success
# tickle weekly Mon/Tue/Wed/Thu/Fri/Sat/Sun say Success
# tickle weekly Thur say Success
# tickle weekly Thurs say Success
# tickle weekly Thursday say Success
# tickle weekly ThuRsDay say Success
# tickle weekly T Th Sa say Success
# tickle weekly T R say Success
# tickle weekly Saturday say Failure
# tickle weekly mon tue wed fri sat sun say Failure
EOF
)

if [ "$results" != "$EXPECTED_RESULTS" ]; then
  echo "$TEST_NAME ... failed"
  exit 1
else
  echo "$TEST_NAME ... passed"
fi
