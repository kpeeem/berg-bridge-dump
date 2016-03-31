#!/bin/sh

while [ 1 ]; do
  /usr/bin/bergcloud_linkd -s
  EXIT_CODE=$?
  # If we've been sigkilled, exit
  if [ $EXIT_CODE -eq 143 -o $EXIT_CODE -eq 137 ]; then
    echo "Wrapper not restarting bergcloud_linkd"
    break
  fi
  echo "Wrapper restarting bergcloud_linkd"
done
