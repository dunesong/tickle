#!/usr/bin/env bash

TEST="test 19: should be able to tickle yearly based on a simple yearday" 

results=$(../tickle.py --date '1970-01-01' 2>&1 <<'EOF'
# tickle yearly 1 say Success
# tickle yearly 1, 2 say Success
# tickle yearly 2 say Failure
# tickle yearly 2, 3, 4 say Failure
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
fi

results=$(../tickle.py --date '1970-01-31' 2>&1 <<'EOF'
# tickle yearly 31 say Success
# tickle yearly 30, 31 say Success
# tickle yearly 1 say Failure
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
fi

results=$(../tickle.py --date '1970-02-01' 2>&1 <<'EOF'
# tickle yearly 32 say Success
# tickle yearly 33 say Failure
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
