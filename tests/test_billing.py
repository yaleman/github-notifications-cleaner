"""tests"""

import pytest
import sys

from github.AuthenticatedUser import AuthenticatedUser
from loguru import logger
from github_notifications_cleaner.billing import get_billing_actions_for_user
from github_notifications_cleaner import Settings, do_login


@pytest.fixture(name="user")
def get_user() -> AuthenticatedUser:
    """fixture to login and get the user etc"""
    settings = Settings()
    if settings.github_username is None:
        logger.error("You need to specify a username in the GITHUB_USERNAME environment variable!")
        sys.exit(1)

    github_client = do_login(Settings())
    user: AuthenticatedUser = github_client.get_user()
    return user


def test_get_billing_actions_for_user(user: AuthenticatedUser) -> None:
    """test get_billing_actions_for_user"""
    get_billing_actions_for_user(user, "octocat")
