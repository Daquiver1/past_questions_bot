#!/bin/bash


FORMAT=true
while [[ $# -gt 0 ]]; do
  case $1 in
    --no-format)
      FORMAT=false
      shift # past argument
      ;;
  esac
done

SCRIPT_DIR=$(dirname "$0")
pushd "$SCRIPT_DIR/.."
source deactivate 2>/dev/null
set -e

if [ $FORMAT = true ]; then
  echo "*** Running black ***"
  poetry run black "./past_question_bot" "./tests"
fi

echo "*** Running mypy ***"
poetry run mypy --show-absolute-path "./past_question_bot" --allow-untyped-decorators --allow-subclassing-any

echo "*** Running pylint ***"
find . -type f -name "*.py" -not -path "./.venv/*" | xargs poetry run pylint  --msg-template='{abspath}:{line}:{column}: {msg_id}: {msg} ({symbol})'
popd
