import os

from github import GithubException
from github_actions_utils.env import github_envs, get_env
from github_actions_utils.github import get_github
from github_actions_utils.log import github_log_group, summary


# def get_gh():
#     actor = os.getenv("GITHUB_ACTOR")
#     assert actor, "Must set GITHUB_ACTOR"
#
#     summary(f"Retrieving {actor} token...", end="")
#     token = os.getenv(actor)
#     if token:
#         actor_token = True
#         summary(":white_check_mark:")
#     else:
#         actor_token = False
#         summary(":x:")
#         summary("Retrieving GITHUB_TOKEN")
#         token = os.getenv("GITHUB_TOKEN")
#     if not token:
#         exit_(f"User '{actor}' is not allowed to auto create Pull Request")
#
#     if actor_token:
#         summary(f"Login in as {actor}...", end="")
#     gh = Github(auth=Token(token))
#     login = gh.get_user().login
#     if login != actor:
#         if actor_token:
#             summary(":x:")
#         exit_(f"Token is for user {login}!")
#     if actor_token:
#         summary(":white_check_mark:")
#     return gh
def exit_(message):  # TODO to github_actions_utils
    print(f"::error::{message}")
    summary(f"ERROR: {message}")
    exit(message)


def github_log_group_context_manager(text):  # TODO to github_actions_utils
    print(f"::group::{text}")
    yield
    print("::endgroup::")


def main():
    actor = github_envs.actor
    with github_log_group_context_manager(f"Logging with {actor}..."):
        actor_token = get_env(actor)
        gh = get_github(actor_token)
        if actor_token and gh.get_user().login != actor:
            exit_(f"Token is for user {gh.get_user().login} not for {actor}!")
    repo = gh.get_current_repo()

    current_branch = github_envs.ref_name
    draft = os.getenv("INPUT_DRAFT") == "true"
    auto_merge = os.getenv("INPUT_AUTO_MERGE") == "true"
    merge_method = os.getenv("INPUT_MERGE_METHOD", "MERGE")

    @github_log_group("Creating PR")
    def _create_pull():
        try:
            pr_ = repo.create_pull(
                repo.default_branch,
                current_branch,
                title=current_branch,
                body="PR automatically created",
                draft=draft,
            )
            print(f"Created PR {pr_.html_url}")
            return pr_
        except GithubException as e:
            errors_messages = [e.get("message", str(e)) for e in e.data["errors"]]
            if len(errors_messages) == 1 and (em := errors_messages[0]).startswith(
                    "A pull request already exists for"
            ):
                print(em)
                return list(repo.get_pulls())[-1]
            raise e

    pr = _create_pull()
    if auto_merge:
        @github_log_group("Setting to auto merge")
        def _auto_merge():
            pr.enable_automerge(merge_method)
            print(f"Auto merge enabled for PR {pr.html_url}")

        _auto_merge()


if __name__ == "__main__":  # pragma: no cover
    main()
