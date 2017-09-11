#!/usr/bin/env bash

TEST="test 21: should be able to tickle yearly on DAY MONTH" 

results=$(../tickle.py --date '1970-01-01' 2>&1 <<'EOF'
# tickle yearly 1 January say Success
# tickle yearly 1 JAN say Success
# tickle yearly 1st jan say Success
# tickle yearly 2 January say Failure
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
# tickle yearly 31 Jan say Success
# tickle yearly 30 Jan say Failure
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
# tickle yearly 01 Feb say Success
# tickle yearly 29 Feb say Failure
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
