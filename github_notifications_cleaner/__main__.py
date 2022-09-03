""" cli """

import sys

import click
from loguru import logger

from . import main


@click.command()
@click.option("-d", "--debug", is_flag=True, default=False, help="Enable debug mode")
def cli(debug: bool = False) -> None:
    """Github Notification Cleaner"""
    logger.remove()
    if debug:
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.add(sys.stderr, level="INFO")
    main()


if __name__ == "__main__":
    cli()
