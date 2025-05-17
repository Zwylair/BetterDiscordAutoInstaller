import os
import sys
import json
import logging
from typing import Optional

import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="(%(asctime)s) %(message)s")


def load_settings():
    try:
        if not os.path.exists(config.SETTINGS_PATH):
            return

        with open(config.SETTINGS_PATH) as f:
            settings = json.load(f)
    except Exception as e:
        logger.error(str(e), exc_info=e)
        sys.exit(1)
    else:
        # BDAI settings
        config.DISCORD_PARENT_PATH = settings.get("discord_installed_path", config.DISCORD_PARENT_PATH)
        config.DISCORD_CANARY_PARENT_PATH = settings.get("discord_canary_installed_path", config.DISCORD_CANARY_PARENT_PATH)
        config.DISCORD_PTB_PARENT_PATH = settings.get("discord_ptb_installed_path", config.DISCORD_PTB_PARENT_PATH)
        config.DISABLE_BDAI_AUTOUPDATE = settings.get("disable_bdai_autoupdate", config.DISABLE_BDAI_AUTOUPDATE)
        config.USE_BD_CI_RELEASES = settings.get("use_betterdiscord_ci_releases", config.USE_BD_CI_RELEASES)
        config.WORKFLOW_RUNS_LIMIT = settings.get("workflow_runs_limit", config.WORKFLOW_RUNS_LIMIT)

        # BD & Discord cached data
        config.DISABLE_DISCORD_VERSION_CHECKING = settings.get("disable_version_check", config.DISABLE_DISCORD_VERSION_CHECKING)
        config.LAST_INSTALLED_DISCORD_VERSION = settings.get("last_installed_discord_version", config.LAST_INSTALLED_DISCORD_VERSION)
        config.LAST_INSTALLED_DISCORD_CANARY_VERSION = settings.get("last_installed_discord_canary_version", config.LAST_INSTALLED_DISCORD_CANARY_VERSION)
        config.LAST_INSTALLED_DISCORD_PTB_VERSION = settings.get("last_installed_discord_ptb_version", config.LAST_INSTALLED_DISCORD_PTB_VERSION)
        config.LAST_INSTALLED_BD_VERSION = settings.get("last_installed_betterdiscord_version", config.LAST_INSTALLED_BD_VERSION)
        config.LAST_INSTALLED_BD_CI_VERSION = settings.get("last_installed_betterdiscord_ci_version", config.LAST_INSTALLED_BD_CI_VERSION)


# noinspection PyTypeChecker
def dump_settings():
    try:
        with open(config.SETTINGS_PATH, "w") as f:
            settings = {
                # BDAI settings
                "discord_installed_path": config.DISCORD_PARENT_PATH,
                "discord_canary_installed_path": config.DISCORD_CANARY_PARENT_PATH,
                "discord_ptb_installed_path": config.DISCORD_PTB_PARENT_PATH,
                "disable_bdai_autoupdate": config.DISABLE_BDAI_AUTOUPDATE,
                "use_betterdiscord_ci_releases": config.USE_BD_CI_RELEASES,
                "workflow_runs_limit": config.WORKFLOW_RUNS_LIMIT,

                # BD & Discord cached data
                "disable_version_check": config.DISABLE_DISCORD_VERSION_CHECKING,
                "last_installed_discord_version": config.LAST_INSTALLED_DISCORD_VERSION,
                "last_installed_discord_canary_version": config.LAST_INSTALLED_DISCORD_CANARY_VERSION,
                "last_installed_discord_ptb_version": config.LAST_INSTALLED_DISCORD_PTB_VERSION,
                "last_installed_betterdiscord_version": config.LAST_INSTALLED_BD_VERSION,
                "last_installed_betterdiscord_ci_version": config.LAST_INSTALLED_BD_CI_VERSION,
            }
            json.dump(settings, f, indent=2)
    except Exception as e:
        logger.error(str(e), exc_info=e)
        sys.exit(1)


def load_github_token():
    try:
        if not os.path.exists(config.GITHUB_TOKEN_FILE_PATH):
            return

        with open(config.GITHUB_TOKEN_FILE_PATH) as f:
            config.GITHUB_TOKEN = json.load(f)
    except Exception as e:
        logger.error(str(e), exc_info=e)
        sys.exit(1)


# noinspection PyTypeChecker
def dump_github_token():
    try:
        with open(config.GITHUB_TOKEN_FILE_PATH, "w") as f:
            json.dump(config.GITHUB_TOKEN, f)
    except Exception as e:
        logger.error(str(e), exc_info=e)
        sys.exit(1)


def set_discord_version(edition: config.DiscordEdition, new_version: str):
    match edition:
        case config.DiscordEdition.STABLE:
            config.LAST_INSTALLED_DISCORD_VERSION = new_version
        case config.DiscordEdition.CANARY:
            config.LAST_INSTALLED_DISCORD_CANARY_VERSION = new_version
        case config.DiscordEdition.PTB:
            config.LAST_INSTALLED_DISCORD_PTB_VERSION = new_version
        case _:
            pass


def get_last_installed_discord_version(edition: config.DiscordEdition) -> Optional[str]:
    match edition:
        case config.DiscordEdition.STABLE:
            return config.LAST_INSTALLED_DISCORD_VERSION
        case config.DiscordEdition.CANARY:
            return config.LAST_INSTALLED_DISCORD_CANARY_VERSION
        case config.DiscordEdition.PTB:
            return config.LAST_INSTALLED_DISCORD_PTB_VERSION
        case _:
            return None
