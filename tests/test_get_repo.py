import pytest

from autocreate import get_repo


@pytest.mark.vcr
def test_get_repo(gh):
    assert get_repo(gh).full_name == "heitorpolidoro/autocreate-pr"
