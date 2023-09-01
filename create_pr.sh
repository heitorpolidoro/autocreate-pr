#!/bin/bash
set -e

token=$(eval echo "\$$GITHUB_ACTOR")
if [[ "$GITHUB_TOKEN" == "" && ("$token" == "$" || "$token" == "") ]]; then
	echo -e "User '$GITHUB_ACTOR' is not allowed to auto create Pull Request"
else
  if [[ "$GITHUB_TOKEN" == "" ]]; then
	  echo "::group::GitHub authentication ($GITHUB_ACTOR)"
	  echo "$token" | gh auth login --with-token
	  gh auth status
	  echo "::endgroup::"
	fi

	echo "::group::Creating Pull Request"
	gh pr create --title "$GITHUB_REF_NAME" --body "PR automatically created" || echo ""
	echo "::endgroup::"

	if [[ "$INPUT_AUTOMERGE" == "true" ]]; then
		echo "::group::Configuring to auto merge"
		gh pr merge --auto --squash
		echo "::endgroup::"
	fi
fi
