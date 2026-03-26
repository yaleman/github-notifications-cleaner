"""tests"""

from github.NamedUser import NamedUser

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
    user: AuthenticatedUser | NamedUser = github_client.get_user()
    assert isinstance(user, AuthenticatedUser)
    return user


# def test_get_billing_actions_for_user(user: AuthenticatedUser) -> None:
#     """test get_billing_actions_for_user, only works if you have access to the 'enhanced billing platform'"""
#     print("Checking billing actions for user: {}".format(user.login))
#     get_billing_actions_for_user(user, user.login)
