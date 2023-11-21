import os
import subprocess

from github import Github, GithubException
from github.Auth import Token
from github.Repository import Repository
from urllib3.util import parse_url

from github_actions_utils.log_utils import github_group


def get_repo(gh: Github) -> Repository:
    url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"])
    repo_name = parse_url(url.decode().strip()).path.replace(".git", "")[1:]
    return gh.get_repo(repo_name)


def main():
    actor = os.getenv("GITHUB_ACTOR")
    assert actor, "Must set GITHUB_ACTOR"
    token = os.getenv(actor) or os.getenv("GITHUB_TOKEN")
    if token:
        # create
        gh = Github(auth=Token(token))
        current_branch = os.getenv("GITHUB_REF_NAME")
        repo = get_repo(gh)
        draft = os.getenv("INPUT_DRAFT") == "true"
        auto_merge = os.getenv("INPUT_AUTO_MERGE") == "true"
        merge_method = os.getenv("INPUT_MERGE_METHOD", "MERGE")

        @github_group("Creating PR")
        def _create_pull():
            try:
                return repo.create_pull(
                    repo.default_branch,
                    current_branch,
                    title=current_branch,
                    body="PR automatically created",
                    draft=draft,
                    # maintainer_can_modify: Opt[bool] = NotSet,
                    # issue: Opt[github.Issue.Issue] = NotSet,
                )
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

            @github_group("Setting to auto merge")
            def _auto_merge():
                pr.enable_automerge(merge_method)

            _auto_merge()
    else:
        exit(f"User '{actor}' is not allowed to auto create Pull Request")


if __name__ == "__main__":  # pragma: no cover
    main()
