import os
from unittest.mock import patch

import pytest
from github import Github, Auth


@pytest.fixture(autouse=True)
def default_envs(monkeypatch):
    monkeypatch.setenv("GITHUB_ACTOR", "test_user")
    monkeypatch.setenv("GITHUB_REF_NAME", "branch")


@pytest.fixture
def gh():
    if token := os.getenv("GITHUB_TOKEN"):
        auth = Auth.Token(token=token)
        return Github(auth=auth)
    return Github()


@pytest.fixture
def repo():
    with patch("github.Repository.Repository") as Repository:
        repository = Repository()
        repository.default_branch = "master"
        with patch("autocreate.get_repo", return_value=repository):
            yield repository


@pytest.fixture
def pr():
    with patch("github.PullRequest.PullRequest") as PullRequest:
        pull_request = PullRequest()
        pull_request.default_branch = "master"
        yield pull_request
