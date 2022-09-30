""" trash code hiding in a trench coat """
import os
import json
from typing import Any, List, Optional


from loguru import logger
from github import Github as GithubAPI
from github.GithubException import UnknownObjectException
from pydantic import BaseSettings, Field


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """settings for this program"""

    github_token: str = Field(..., env="GITHUB_TOKEN")
    github_username: Optional[str] = Field(None, env="GITHUB_USERNAME")

    ignored_repos: List[str] = Field([], env="IGNORED_REPOS")

    class Config:
        """config subclass"""

        # enable .env file support
        env_file = ".env"
        env_file_encoding = "utf-8"

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            """figures out the multi-env-var thing"""
            if field_name == "ignored_repos":
                return [x.lower() for x in raw_val.split(",")]
            return json.loads(raw_val)


def do_login(settings: Settings) -> GithubAPI:
    """does the login/auth bit"""

    if settings.github_token:
        logger.debug("Using GITHUB_TOKEN environment variable for login.")
        github: GithubAPI = GithubAPI(os.getenv("GITHUB_TOKEN"))
        return github
    raise ValueError("No authentication method was found!")


def main() -> None:
    """look, I can't be held responsible for all my code."""

    my_settings = Settings()

    try:
        github = do_login(my_settings)
    except ValueError as value_error:
        logger.error("{}", value_error)
        return
    current_user = github.get_user()

    notifications = current_user.get_notifications()
    logger.info("{} notifications", notifications.totalCount)

    for notification in notifications:
        if notification.repository.full_name.lower() in my_settings.ignored_repos:
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
                        "type: {} state: {}",
                        notification.subject.type,
                        pull_request.state,
                    )
                    if pull_request.state == "closed":
                        notification.mark_as_read()
                        logger.success(
                            "Marking {} - {} read!",
                            notification.repository.full_name,
                            notification.subject.title,
                        )
            else:
                logger.warning(
                    json.dumps(
                        {
                            "message": "unhandled type",
                            "type": notification.subject.type,
                            "title": notification.subject.title,
                        }
                    )
                )
