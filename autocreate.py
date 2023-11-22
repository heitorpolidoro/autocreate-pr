import os
import subprocess

from github import Github, GithubException
from github.Auth import Token
from github.Repository import Repository
from github_actions_utils.log import github_log_group, summary
from urllib3.util import parse_url


def get_repo(gh: Github) -> Repository:
    url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"])
    repo_name = parse_url(url.decode().strip()).path.replace(".git", "")[1:]
    return gh.get_repo(repo_name)


def exit_(message):  # TODO to github_actions_utils
    summary(f"ERROR: {message}")
    exit(message)


def get_gh():
    actor = os.getenv("GITHUB_ACTOR")
    assert actor, "Must set GITHUB_ACTOR"

    summary(f"Retrieving {actor} token...", end="")
    token = os.getenv(actor)
    if token:
        actor_token = True
        summary(":white_check_mark:")
    else:
        actor_token = False
        summary(":x:")
        summary("Retrieving GITHUB_TOKEN")
        token = os.getenv("GITHUB_TOKEN")
    if not token:
        exit_(f"User '{actor}' is not allowed to auto create Pull Request")

    if actor_token:
        summary(f"Login in as {actor}...", end="")
    gh = Github(auth=Token(token))
    login = gh.get_user().login
    if login != actor:
        if actor_token:
            summary(":x:")
        exit_(f"Token is for user {login}!")
    if actor_token:
        summary(":white_check_mark:")
    return gh


def main():
    gh = get_gh()
    repo = get_repo(gh)

    current_branch = os.getenv("GITHUB_REF_NAME")
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
                # maintainer_can_modify: Opt[bool] = NotSet,
                # issue: Opt[github.Issue.Issue] = NotSet,
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
