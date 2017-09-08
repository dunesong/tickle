#!/usr/bin/env bash

TEST="test 16: should be able to tickle monthly on nth weekday"

results=$(../tickle.py --date '1970-01-01' 2>&1 <<'EOF'
# tickle monthly 1st Thursday say Success
# tickle monthly first thu say Success
# tickle monthly 1 th say Success
# tickle monthly 1st Friday say Failure
# tickle monthly 2nd Thursday say Failure
# tickle monthly second Thursday, third Friday say Failure
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
# tickle monthly 1st Thursday say Failure
# tickle monthly fifth Friday say Success
# tickle monthly 5TH FRI say Success
# tickle monthly 4th wed, 5th fri say Success
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
else
  echo "$TEST ... passed"
fi
