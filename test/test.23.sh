#!/usr/bin/env bash

TEST="test 23: should be able to tickle within a date range (FROM ... UNTIL ...)" 

results=$(../tickle.py --date '1970-01-01' 2>&1 <<'EOF'
# tickle daily from 1969-12-31 say Success
# tickle daily from 1970-01-01 say Success
# tickle daily from 1970-01-02 say Failure
# tickle daily until 1970-01-02 say Success
# tickle daily until 1970-01-01 say Success
# tickle daily until 1969-12-31 say Failure
# tickle daily from 1969-12-30 until 1969-12-31 say Failure
# tickle daily from 1969-12-31 until 1970-01-01 say Success
# tickle daily from 1970-01-01 until 1970-01-01 say Success
# tickle daily from 1970-01-01 until 1970-01-02 say Success
# tickle daily from 1970-01-02 until 1970-01-03 say Failure
EOF
)

EXPECTED_RESULTS=$(cat <<'EOF'
Success
Success
Success
Success
Success
Success
Success
EOF
)

if [ "$results" != "$EXPECTED_RESULTS" ]; then
  echo "$TEST ... failed"
  exit 1
else
  echo "$TEST ... passed"
fi
