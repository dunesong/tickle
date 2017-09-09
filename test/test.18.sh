#!/usr/bin/env bash

TEST="test 18: should be able to tickle monthly based on the last day"

results=$(../tickle.py --date '1970-01-31' 2>&1 <<'EOF'
# tickle monthly last day say Success
# tickle monthly 0 days before last day say Success
# tickle monthly 0days before last day say Success
# tickle monthly 0day before last day say Success
# tickle monthly 0d before last day say Success
# tickle monthly 1 day before last day say Failure
EOF
)

EXPECTED_RESULTS=$(cat <<'EOF'
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
fi

results=$(../tickle.py --date '1970-01-21' 2>&1 <<'EOF'
# tickle monthly 10 day before last day say Success
# tickle monthly 10 days before last day say Success
# tickle monthly 11 days before last day say Failure
# tickle monthly 31 days before last day say Failure
# tickle monthly last day say Failure
# tickle monthly 0 days before last day say Failure
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
