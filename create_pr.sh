#!/bin/bash
BOLD='\x1b[1m'
NORMAL="\x1b[0m"

echo "::group::Workaround"
git config --global --add safe.directory /github/workspace
echo "::endgroup::"

set -e
token=$(eval echo "\$$GITHUB_ACTOR")
if [[ -z "$token" ]]; then
	echo -e "User $BOLD$GITHUB_ACTOR$NORMAL is not allowed to auto create Pull Request"
else
	echo "::group::GitHub authentication ($GITHUB_ACTOR)"
	eval echo "\$$GITHUB_ACTOR" | gh auth login --with-token
	gh auth status
	echo "::endgroup::"

	echo "::group::Creating Pull Request"
	gh pr create --title "$GITHUB_REF_NAME" --body "PR automatically created" || echo ""
	echo "::endgroup::"
fi
