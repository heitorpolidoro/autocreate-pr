#!/bin/bash
# Set of functions to allow create tests for bash/shell scripts
VERSION=0.1.0
# Array of ENV vars. Used to unset ENV vars after each test
TEMP_ENVS=()

###################################################################################################
# Return true if 2 strings are equals or false otherwise printing the values, actual and expected,
# the file and the line the assert was called
# ARGUMENTS:
#   actual: The string you are checking
#   expected: The string, or regex, you expected that match equals with actual
# OUTPUTS:
#   If the 2 string doesn't match, print the file, function name and line where the assert was
#   called, and the expected and actual parameters
# RETURN:
#   true if the 2 strings have a match, false otherwise
###################################################################################################
function assert {
	actual=$1
	expected=$2
	# shellcheck disable=SC2053
	if [[ $actual = $expected ]]; then
		true
	else
		echo "${BASH_SOURCE[1]} failed in function '${FUNCNAME[1]}' at line ${BASH_LINENO[0]}."
		echo -e "EXPECTED:\n${expected}\nACTUAL:\n${actual}\n"
		false
	fi
}
###################################################################################################
# Mock a command or a function printing the received parameters
# ARGUMENTS:
#   function_name: The of the function, or command, to mock
# OUTPUTS:
#   The parameters to the function
###################################################################################################
function mock {
	function_name=$1
	shift
	return_function=$*
	function mocked_return {
		echo -n "Mocked $function_name###params=$*###"
	}
	if [[ -z "$return_function" ]];
	then
	  return_function=mocked_return
	else
	  if [[ $(type -t $return_function) != function ]];
	  then
	    return_function="echo $return_function"
	  fi
	fi

	# shellcheck disable=SC2139
	# shellcheck disable=SC2140
	alias "$function_name"="$return_function"
}

###################################################################################################
# Set an environment variable to use only in the test case.
# ARGUMENTS:
#   name: The name of the environment variable
#   value: The value of the variable
###################################################################################################
function set_env {
	env_name=$1
	env_value=$2

	export "$env_name"="$env_value"
	TEMP_ENVS+=("$env_name")
}

###################################################################################################
# Run all the functions starting with "test_"
# OUTPUTS:
#   The result of each test
# RETURN:
#   0 if all the tests results is "OK", 1 otherwise
###################################################################################################
function run_tests {
	error_code=0
	for test_function in $(declare -F); do
		if [[ "$test_function" = "test_"* ]]; then
			if $test_function; then
				result="OK"
			else
				result="ERROR"
				error_code=1
			fi
			for t_env in "${TEMP_ENVS[@]}"; do
				unset "$t_env"
			done
			TEMP_ENVS=()
			echo -e "$test_function\t$result"
		fi
	done
	exit $error_code
}


# shellcheck disable=SC2206
should_update() {
  NEW_VERSION=$1
  OLDIFS=$IFS
  IFS=. cur_version=($VERSION)
  IFS=. new_version=($NEW_VERSION)
  for (( i=0; i<${#cur_version[@]}; i++ )); do
    if [[ ${cur_version[i]} -lt ${new_version[i]} ]]; then
      return 0
    fi
  done
  IFS=$OLDIFS
  return 1
}
update() {
  NEW_VERSION="1.10.0"
  set -e
  echo "Checking for updates..."
  if should_update $NEW_VERSION; then
    echo "Updating to version $NEW_VERSION"
  fi
  exit 0
}
###################################################################################################
# Argument parser
###################################################################################################
while [[ $# -gt 0 ]]; do
  arg="$1"
  case $arg in
    -h|--help)
      echo "Usage: $0 [-h|--help] [--no-run-tests]"
      exit 0
      ;;

    --version)
      echo "Bashtest version: ${VERSION}"
      exit 0
      ;;

    update)
      update
      ;;

    *)
      echo "Unknown option $1"
      exit 1
      ;;

  esac
done
