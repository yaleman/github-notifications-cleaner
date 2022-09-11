""" playing with billing """

import json
import os
import sys
from typing import Any, Dict

from github.AuthenticatedUser import AuthenticatedUser
from loguru import logger

from . import do_login, Settings


def get_billing_actions_for_user(user_object: AuthenticatedUser, username: str) -> Dict[str, Any]:
    """
    :calls: `GET /users/{username}/settings/billing/actions <https://docs.github.com/en/rest/billing#get-github-actions-billing-for-a-user>`_
    :rtype: Dict
    """
    assert isinstance(username, str), username
    url = f"/users/{username}/settings/billing/actions"

    #pylint: disable=protected-access
    data: Dict[str, Any] = user_object._requester.requestJsonAndCheck("GET", url)[1] # type: ignore

    return data

def get_billing_packages_for_user(user_object: AuthenticatedUser, username: str) -> Dict[str, Any]:
    """
    :calls: `GET /users/{username}/settings/billing/packages <https://docs.github.com/en/rest/billing#get-github-actions-billing-for-a-user>`_
    :rtype: Dict
    """
    assert isinstance(username, str), username
    url = f"/users/{username}/settings/billing/packages"

    #pylint: disable=protected-access
    data: Dict[str, Any] = user_object._requester.requestJsonAndCheck("GET", url)[1] # type: ignore

    return data

def get_billing_storage_for_user(user_object: AuthenticatedUser, username: str) -> Dict[str, Any]:
    """
    :calls: `GET /users/{username}/settings/billing/shared-storage <https://docs.github.com/en/rest/billing#get-github-actions-billing-for-a-user>`_
    :rtype: Dict
    """
    assert isinstance(username, str), username
    url = f"/users/{username}/settings/billing/shared-storage"

    #pylint: disable=protected-access
    data: Dict[str, Any] = user_object._requester.requestJsonAndCheck("GET", url)[1] # type: ignore

    return data

logger.remove()
logger.add(sys.stdout, level=os.getenv("LOG_LEVEL", "INFO"))
gh = do_login(Settings())
user = gh.get_user()
billing_data = get_billing_actions_for_user(user, "yaleman")
print(json.dumps(billing_data))
billing_data = get_billing_packages_for_user(user, "yaleman")
print(json.dumps(billing_data))
billing_data = get_billing_storage_for_user(user, "yaleman")
print(json.dumps(billing_data))
