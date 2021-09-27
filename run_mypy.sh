#!/bin/bash

NUM_ERRORS="0"

FILES="$(find . -type f -name '*.py')"
for FILE in $FILES; do
  mypy "$FILE"
  num_errors="$((NUM_ERRORS + $?))"
done

exit "$NUM_ERRORS"
