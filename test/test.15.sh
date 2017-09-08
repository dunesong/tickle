#!/usr/bin/env bash

TEST="test 15: should be able to tickle monthly on integer days of the month"

results=$(../tickle.py --date '1970-01-01' 2>&1 <<'EOF'
# tickle monthly 1 say Success
# tickle monthly 2 say Failure
# tickle monthly 1,2, 3 , 4 say Success
# tickle monthly 2,1 say Success
# tickle monthly 01 say Success
EOF
)

EXPECTED_RESULTS=$(cat <<'EOF'
Success
Success
Success
Success
EOF
)

if [ "$results" != "$EXPECTED_RESULTS" ]; then
  echo "$TEST ... failed"
  exit 1
fi

results=$(../tickle.py --date '1970-01-15' 2>&1 <<'EOF'
# tickle monthly 1 say Failure
# tickle monthly 15 say Success
# tickle monthly 1, 15 say Success
EOF
)

EXPECTED_RESULTS=$(cat <<'EOF'
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
