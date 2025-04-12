# github-notifications-cleaner

This cleans up notifications from merged PRs if they're closed, because dependabot is a noisy notification-spamming thing.

## Installation

Install this library using `pip`:

    python -m pip install git+https://github.com/yaleman/github-notifications-cleaner

## Usage

Environment variables:

- GITHUB_TOKEN - your auth token, which needs notification access
- IGNORED_REPOS - a comma-delimited list of repositories to ignore, ie "yaleman/test,kanidm/kanidm" etc

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:

    cd github-notifications-cleaner
    uv venv
    source .venv/bin/activate
