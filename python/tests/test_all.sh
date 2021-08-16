#!/bin/sh
DIRECTORY=$(cd `dirname $0` && pwd)
EXEC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

check_arr=()
cd "${DIRECTORY}"
for filename in *; do
  if [[ "${filename}" =~ "_test.py" ]]; then
    echo "TESTING ${filename}"
    ./${filename}
    result=$?
    if [[ "${result}" == 1 ]]; then
      check_arr+=("${filename}")
    fi
    echo "--------------------------------------------------"
  fi
done

cd "${EXEC_DIR}"
if [[ "${#check_arr[@]}" == 0 ]]; then
  echo "ALL TESTS PASSING"
  exit 0
else
  echo "~~~~~~~~~~~~~~~~~~~~~~~FAILURES~~~~~~~~~~~~~~~~~~~~~~~"
  for filename in ${check_arr}; do
    echo "    ${filename}"
  done
  echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
  exit 1
fi
