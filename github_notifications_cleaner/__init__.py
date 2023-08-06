""" trash code hiding in a trench coat """
import os
import sys
from typing import Any, List, Optional

from loguru import logger
from github import Github as GithubAPI
from github.GithubException import UnknownObjectException
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """settings for this program"""

    github_token: str = Field(..., validation_alias="GITHUB_TOKEN")
    github_username: Optional[str] = Field(None, validation_alias="GITHUB_USERNAME")

    ignored_repos: str = Field(
        default="",
        validation_alias="IGNORED_REPOS",
        help="comma separated list of repos to ignore",
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def ignored_repos_split(self) -> List[str]:
        """split the ignored repos becuase pydantic was being a jerk"""
        return self.ignored_repos.split(",")


def do_login(settings: Settings) -> GithubAPI:
    """does the login/auth bit"""

    if settings.github_token:
        logger.debug("Using GITHUB_TOKEN environment variable for login.")
        github: GithubAPI = GithubAPI(os.getenv("GITHUB_TOKEN"))
        return github
    raise ValueError("No authentication method was found!")


def setup_logging() -> None:
    """does what it says on the tin"""

    if not sys.stdout.isatty():

        def formatter(_record: Any) -> str:
            """this function returns the string to be formatted, not the actual message to be logged"""
            return "{message}"

        logger.remove()
        logger.add(sys.stdout, level="INFO", serialize=True, format=formatter)


def main() -> None:
    """look, I can't be held responsible for all my code."""

    setup_logging()

    my_settings = Settings()

    try:
        github = do_login(my_settings)
    except ValueError as value_error:
        logger.error(value_error)
        return

    current_user = github.get_user()

    notifications = current_user.get_notifications()
    logger.info({"notifications": notifications.totalCount})

    for notification in notifications:
        if (
            notification.repository.full_name.lower()
            in my_settings.ignored_repos_split()
        ):
            logger.debug(
                "Skipping ignored repo: {} {} - {}",
                notification.id,
                notification.repository.full_name,
                notification.subject.title,
            )
            continue
        logger.debug(
            "{} {} - {}",
            notification.id,
            notification.repository.full_name,
            notification.subject.title,
        )

        if notification.unread:
            if notification.subject.type == "PullRequest":
                try:
                    pull_request = notification.get_pull_request()
                except UnknownObjectException as missing_pr:
                    logger.error(
                        "Couldn't get PR: {} - error: {}", str(notification), missing_pr
                    )
                    continue

                except Exception as generic_exception:  # pylint: disable=broad-except
                    logger.error(
                        "Couldn't get PR: {} - error: {}",
                        str(notification),
                        generic_exception,
                    )
                    continue
                if pull_request.state != "open":
                    logger.debug(
                        {
                            "type": notification.subject.type,
                            "state": pull_request.state,
                        }
                    )
                    if pull_request.state == "closed":
                        notification.mark_as_read()
                        logger.success(
                            "Marking {} - {} read!",
                            notification.repository.full_name,
                            notification.subject.title,
                        )
            elif notification.subject.type == "CheckSuite":
                logger.debug("Ignoring CheckSuite Status: {}", notification.raw_data)

            else:
                logger.warning(
                    {
                        "message": "unhandled type",
                        "type": notification.subject.type,
                        "title": notification.subject.title,
                    }
                )
