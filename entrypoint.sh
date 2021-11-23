#!/bin/bash
BOLD='\x1b[1m'
NORMAL="\x1b[0m"

set -e
echo "::group::GitHub authentication"
  echo "$INPUT_PERSONAL_ACCESS_TOKEN" | gh auth login --with-token
echo "::endgroup::"

echo "::group::Creating PullR"
  gh pr create --title "$GITHUB_REF_NAME" --body "PR Automated created" || echo ""
echo "::endgroup::"

if [[ "$INPUT_AUTOMERGE" == "true" ]]
then
  if [[ "$GITHUB_REPOSITORY_OWNER" != "${GITHUB_ACTOR}" ]]
  then
    echo -e "User $BOLD$GITHUB_ACTOR$NORMAL is not allowed to auto-release"
  else
    echo "::group::Setting to Automerge"
      gh pr merge --auto --squash --delete-branch
    echo "::endgroup::"
  fi
fi