""" tests the settings loader """

import os
from unittest import mock

import pytest
from github_notifications_cleaner import Settings


def test_settings_token() -> None:
    """tests ... not much"""
    if os.getenv("GITHUB_TOKEN") is None:
        with pytest.raises(ValueError):
            Settings()
    else:
        pytest.skip("GITHUB_TOKEN had a value")

@mock.patch.dict(os.environ, {"GITHUB_TOKEN": "lulz"})
def test_settings_username() -> None:
    """tests ... not much"""
    if os.getenv("GITHUB_USERNAME") is None:
        settings = Settings()
        assert settings.github_username is None
    else:
        settings = Settings()
        assert settings.github_username is not None
        print(f"found username: {settings.github_username}")
