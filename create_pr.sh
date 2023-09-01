#!/bin/bash
set -e
if [[ "$INPUT_ENABLE_TO_ALL" == "true" ]]; then
  echo "all"
  exit 1
fi
token=$(eval echo "\$$GITHUB_ACTOR")
if [[ "$token" == "$" || "$token" == "" ]]; then
	echo -e "User '$GITHUB_ACTOR' is not allowed to auto create Pull Request"
else
	echo "::group::GitHub authentication ($GITHUB_ACTOR)"
	eval echo "\$$GITHUB_ACTOR" | gh auth login --with-token
	gh auth status
	echo "::endgroup::"

	echo "::group::Creating Pull Request"
	gh pr create --title "$GITHUB_REF_NAME" --body "PR automatically created" || echo ""
	echo "::endgroup::"

	if [[ "$INPUT_AUTOMERGE" == "true" ]]; then
		echo "::group::Configuring to auto merge"
		gh pr merge --auto --squash
		echo "::endgroup::"
	fi
fi
