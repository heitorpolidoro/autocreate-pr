# shellcheck disable=SC1090
source <(curl -s https://raw.githubusercontent.com/heitorpolidoro/bashtest/master/bashtest.sh)

# Set up mock
mock git
mock gh

test_without_github_user() {
  result=$(source create_pr.sh)
  assert "$result" "*User '' is not allowed to auto create Pull Request*"
}

test_with_github_user_without_permission() {
  set_env GITHUB_ACTOR 'test'
  result=$(source create_pr.sh)
  assert "$result" "*User 'test' is not allowed to auto create Pull Request*"
}

test_gh_login() {
  set_env GITHUB_ACTOR 'test'
  set_env test 'token'
  result=$(source create_pr.sh)
  assert "$result" "*GitHub authentication (test)*"
}

test_pr_create() {
  set_env GITHUB_ACTOR 'test'
  set_env test 'token'
  set_env GITHUB_REF_NAME 'GITHUB_REF_NAME'
  result=$(source create_pr.sh)
  assert "$result" "*###params=pr create --title GITHUB_REF_NAME --body PR automatically created###*"
}

test_automerge() {
  set_env GITHUB_ACTOR 'test'
  set_env test 'token'
  set_env INPUT_AUTOMERGE true
  result=$(source create_pr.sh)
  assert "$result" "*###params=pr merge --auto --squash###*"
}

run_tests
