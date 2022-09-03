""" trash code hiding in a trench coat """
import os
import json
from typing import Any, List


from loguru import logger
from github import Github as GithubAPI
from pydantic import BaseSettings, Field


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """settings for this program"""

    github_token: str = Field(..., env="GITHUB_TOKEN")

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
                pull_request = notification.get_pull_request()
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
                logger.warning("Ooh we have a {}", notification.subject.type)
                logger.warning(notification.subject.title)
        else:
            logger.debug("unread: {}", notification.unread)
