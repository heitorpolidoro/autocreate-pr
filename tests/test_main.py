import os
from unittest.mock import patch

import pytest
from github import GithubException

from autocreate import main


@pytest.fixture
def actor_token(monkeypatch):
    monkeypatch.setenv("test_user", os.getenv("GITHUB_TOKEN", "actor_token"))


def test_missing_github_actor(monkeypatch):
    monkeypatch.delenv("GITHUB_ACTOR")
    with pytest.raises(AssertionError) as error:
        main()

    assert str(error.value) == "Must set GITHUB_ACTOR"


def test_without_github_user(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", False)
    with pytest.raises(SystemExit) as error:
        main()

    assert (
        str(error.value)
        == "User 'test_user' is not allowed to auto create Pull Request"
    )


def test_create_pull_request(actor_token, repo):
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
    main()

    repo.create_pull.assert_called_once_with(
        "master",
        "branch",
        title="branch",
        body="PR automatically created",
        draft=False,
    )

    repo.create_pull.return_value.enable_automerge.assert_called_once_with("MERGE")


def test_already_created_pull_request(actor_token, repo, pr, monkeypatch, capsys):
    repo.create_pull.side_effect = GithubException(
        422,
        data={
            "errors": [
                {"message": "A pull request already exists for heitorpolidoro:branch."}
            ]
        },
    )
    repo.get_pulls.return_value = [pr]
    monkeypatch.setenv("INPUT_AUTO_MERGE", "true")
    main()

    assert (
        "A pull request already exists for heitorpolidoro:branch."
        in capsys.readouterr().out
    )

    repo.create_pull.assert_called_once_with(
        "master",
        "branch",
        title="branch",
        body="PR automatically created",
        draft=False,
    )

    pr.enable_automerge.assert_called_once_with("MERGE")


def test_other_error(actor_token, repo, monkeypatch, capsys):
    repo.create_pull.side_effect = GithubException(
        422,
        data={
            "errors": [
                {"message": "Something went wrong"}
            ]
        },
    )
    monkeypatch.setenv("INPUT_AUTO_MERGE", "true")
    with pytest.raises(Exception) as error:
        main()

    assert "Something went wrong" in str(error)

    repo.create_pull.assert_called_once_with(
        "master",
        "branch",
        title="branch",
        body="PR automatically created",
        draft=False,
    )

    repo.create_pull.return_value.enable_automerge.assert_not_called()
