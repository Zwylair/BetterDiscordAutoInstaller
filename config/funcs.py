import os
import sys
import json
import logging

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
        config.DISABLE_BDAI_AUTOUPDATE = settings.get("disable_bdai_autoupdate", config.DISABLE_BDAI_AUTOUPDATE)
        config.USE_BD_CI_RELEASES = settings.get("use_betterdiscord_ci_releases", config.USE_BD_CI_RELEASES)

        # BD & Discord cached data
        config.DISABLE_DISCORD_VERSION_CHECKING = settings.get("disable_version_check", config.DISABLE_DISCORD_VERSION_CHECKING)
        config.LAST_INSTALLED_DISCORD_VERSION = settings.get("last_installed_discord_version", config.LAST_INSTALLED_DISCORD_VERSION)
        config.LAST_INSTALLED_BD_VERSION = settings.get("last_installed_betterdiscord_version", config.LAST_INSTALLED_BD_VERSION)
        config.LAST_INSTALLED_BD_CI_VERSION = settings.get("last_installed_betterdiscord_ci_version", config.LAST_INSTALLED_BD_CI_VERSION)


# noinspection PyTypeChecker
def dump_settings():
    try:
        with open(config.SETTINGS_PATH, "w") as f:
            settings = {
                # BDAI settings
                "discord_installed_path": config.DISCORD_PARENT_PATH,
                "disable_bdai_autoupdate": config.DISABLE_BDAI_AUTOUPDATE,
                "use_betterdiscord_ci_releases": config.USE_BD_CI_RELEASES,

                # BD & Discord cached data
                "disable_version_check": config.DISABLE_DISCORD_VERSION_CHECKING,
                "last_installed_discord_version": config.LAST_INSTALLED_DISCORD_VERSION,
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
