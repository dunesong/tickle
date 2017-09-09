#!/usr/bin/env bash

TEST="test 20: should be able to tickle yearly on MONTH DAY" 

results=$(../tickle.py --date '1970-01-01' 2>&1 <<'EOF'
# tickle yearly January 1 say Success
# tickle yearly JAN 1 say Success
# tickle yearly jan 1st say Success
# tickle yearly January 2 say Failure
EOF
)

EXPECTED_RESULTS=$(cat <<'EOF'
Success
Success
Success
EOF
)

if [ "$results" != "$EXPECTED_RESULTS" ]; then
  echo "$TEST ... failed"
  exit 1
fi

results=$(../tickle.py --date '1970-01-31' 2>&1 <<'EOF'
# tickle yearly Jan 31 say Success
# tickle yearly Jan 30 say Failure
EOF
)

EXPECTED_RESULTS=$(cat <<'EOF'
Success
EOF
)

if [ "$results" != "$EXPECTED_RESULTS" ]; then
  echo "$TEST ... failed"
  exit 1
fi

results=$(../tickle.py --date '1970-02-01' 2>&1 <<'EOF'
# tickle yearly Feb 01 say Success
# tickle yearly Feb 29 say Failure
EOF
)

EXPECTED_RESULTS=$(cat <<'EOF'
Success
EOF
)

if [ "$results" != "$EXPECTED_RESULTS" ]; then
  echo "$TEST ... failed"
  exit 1
else
  echo "$TEST ... passed"
fi
