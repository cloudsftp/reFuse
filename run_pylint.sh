#!/bin/bash

RCFILE="etc/pylint_config.rc"

NUM_ERRORS="0"

FILES="$(find . -type f -name '*.py')"
for FILE in $FILES; do
  pylint --rcfile "$RCFILE" "$FILE"
  NUM_ERRORS="$((NUM_ERRORS + $?))"
done

exit "$NUM_ERRORS"
