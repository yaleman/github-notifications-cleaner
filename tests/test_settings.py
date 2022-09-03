""" tests the settings loader """

import os
import pytest
from github_notifications_cleaner import Settings


def test_settings() -> None:
    """ tests ... not much """
    if os.getenv("GITHUB_TOKEN") is None:
        with pytest.raises(ValueError):
            Settings()
