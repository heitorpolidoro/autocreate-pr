import os
from unittest.mock import patch

import pytest

from autocreate import main


@pytest.fixture
def actor_token(monkeypatch):
    monkeypatch.setenv("test_user", os.getenv("GITHUB_TOKEN", "actor_token"))


def test_missing_github_actor(monkeypatch):
    monkeypatch.delenv("GITHUB_ACTOR")
    with pytest.raises(AssertionError) as error:
        main()


def test_without_github_user(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", False)
    with pytest.raises(SystemExit) as error:
        main()

    assert (
        str(error.value)
        == "User 'test_user' is not allowed to auto create Pull Request"
    )


def test_create_pull_request(actor_token, repo):
    with patch("autocreate.get_repo", return_value=repo):
        main()

    repo.create_pull.assert_called_once_with(
        "master",
        "branch",
        title="branch",
        body="PR automatically created",
        draft=False,
    )


def test_create_pull_request_draft(actor_token, repo, monkeypatch):
    monkeypatch.setenv("INPUT_DRAFT", "true")
    with patch("autocreate.get_repo", return_value=repo):
        main()

    repo.create_pull.assert_called_once_with(
        "master",
        "branch",
        title="branch",
        body="PR automatically created",
        draft=True,
    )


def test_create_pull_request_auto_merge(actor_token, repo, monkeypatch):
    monkeypatch.setenv("INPUT_AUTO_MERGE", "true")
    with patch("autocreate.get_repo", return_value=repo):
        main()

    repo.create_pull.assert_called_once_with(
        "master",
        "branch",
        title="branch",
        body="PR automatically created",
        draft=False,
    )

    repo.create_pull.return_value.merge.assert_called_once_with(auto_merge=True)
