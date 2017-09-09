#!/usr/bin/env bash

TEST="test 17: should be able to tickle monthly on nth last weekday"

results=$(../tickle.py --date '1970-01-01' 2>&1 <<'EOF'
# tickle monthly 5th last Thursday say Success
# tickle monthly 5th last thu say Success
# tickle monthly 5 last thu say Success
# tickle monthly last Thursday say Failure
# tickle monthly 5th last fri say Failure
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

results=$(../tickle.py --date '1970-01-30' 2>&1 <<'EOF'
# tickle monthly last Friday say Success
# tickle monthly first last Friday say Success
# tickle monthly 1st last FRI say Success
# tickle monthly 4th wed, last fri say Success
# tickle monthly last Thursday say Failure
# tickle monthly fifth last fri say Failure
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
else
  echo "$TEST ... passed"
fi
