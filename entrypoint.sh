#!/bin/bash
BOLD='\x1b[1m'
NORMAL="\x1b[0m"

set -e
echo "::group::GitHub authentication"
  echo "$GITHUB_ACTOR"
  eval echo "\$$GITHUB_ACTOR"
  eval echo "\$$GITHUB_ACTOR" | gh auth login --with-token
  gh auth status
echo "::endgroup::"

echo "::group::Creating Pull Request"
  gh pr create --title "$GITHUB_REF_NAME" --body "PR Automated created" || echo ""
echo "::endgroup::"
