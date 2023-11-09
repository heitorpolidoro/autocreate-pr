import os
import subprocess

from github import Github
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
        gh = Github(token)
        current_branch = os.getenv("GITHUB_REF_NAME")
        repo = get_repo(gh)

        @github_group("Creating PR")
        def _create_pull():
            return repo.create_pull(
                repo.default_branch,
                current_branch,
                title=current_branch,
                body="PR automatically created",
                draft=os.getenv("INPUT_DRAFT") == "true",
                # maintainer_can_modify: Opt[bool] = NotSet,
                # issue: Opt[github.Issue.Issue] = NotSet,
            )

        _create_pull()
    else:
        exit(f"User '{actor}' is not allowed to auto create Pull Request")


if __name__ == "__main__":  # pragma: no cover
    main()
