""" playing with billing """

import json
import os
import sys
from typing import Any, Dict

from github.GithubException import UnknownObjectException
from github.AuthenticatedUser import AuthenticatedUser
from loguru import logger

from . import do_login, Settings


def get_billing_actions_for_user(
    user_object: AuthenticatedUser, username: str
) -> Dict[str, Any]:
    """
    :calls: `GET /users/{username}/settings/billing/actions <https://docs.github.com/en/rest/billing#get-github-actions-billing-for-a-user>`_
    :rtype: Dict
    """
    assert isinstance(username, str), username
    url = f"/users/{username}/settings/billing/actions"

    # pylint: disable=protected-access
    actions_data: Dict[str, Any] = user_object._requester.requestJsonAndCheck("GET", url)[1]  # type: ignore

    return actions_data


def get_billing_packages_for_user(
    user_object: AuthenticatedUser, username: str
) -> Dict[str, Any]:
    """
    :calls: `GET /users/{username}/settings/billing/packages <https://docs.github.com/en/rest/billing#get-github-actions-billing-for-a-user>`_
    :rtype: Dict
    """
    assert isinstance(username, str), username
    url = f"/users/{username}/settings/billing/packages"

    # pylint: disable=protected-access
    packages_data: Dict[str, Any] = user_object._requester.requestJsonAndCheck("GET", url)[1]  # type: ignore

    return packages_data


def get_billing_storage_for_user(
    user_object: AuthenticatedUser, username: str
) -> Dict[str, Any]:
    """
    :calls: `GET /users/{username}/settings/billing/shared-storage <https://docs.github.com/en/rest/billing#get-github-actions-billing-for-a-user>`_
    :rtype: Dict
    """
    assert isinstance(username, str), username
    url = f"/users/{username}/settings/billing/shared-storage"

    # pylint: disable=protected-access
    storage_data: Dict[str, Any] = user_object._requester.requestJsonAndCheck("GET", url)[1]  # type: ignore

    return storage_data

def cli() -> None:
    """ dumps all your billing data """
    logger.remove()
    logger.add(sys.stdout, level=os.getenv("LOG_LEVEL", "INFO"))

    settings = Settings()
    if settings.github_username is None:
        logger.error(
            "You need to specify a username in the GITHUB_USERNAME environment variable!"
        )
        sys.exit(1)

    github_client = do_login(Settings())
    user = github_client.get_user()
    for func in [
        get_billing_actions_for_user,
        get_billing_packages_for_user,
        get_billing_storage_for_user,
    ]:
        try:
            data = func(user, settings.github_username)
            print(json.dumps(data))
        except UnknownObjectException as uoe:
            logger.error("Couldn't get actions billing data - does the token have access?")
            logger.debug(uoe)

if __name__ == '__main__':
    cli()
