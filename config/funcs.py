import os
import sys
import json
import logging

import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='(%(asctime)s) %(message)s')

def load_settings():
    try:
        settings = json.load(open(config.SETTINGS_PATH)) if os.path.exists(config.SETTINGS_PATH) else {}
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)
    else:
        config.DISCORD_PARENT_PATH = settings.get('discord_installed_path', None)
        config.LAST_INSTALLED_DISCORD_VERSION = settings.get('last_installed_discord_version', None)
        config.DISABLE_DISCORD_VERSION_CHECKING = settings.get('disable_version_check', False)
        config.DISABLE_BDAI_AUTOUPDATE = settings.get('disable_bdai_autoupdate', False)
        config.LAST_INSTALLED_BETTERDISCORD_VERSION = settings.get('last_installed_betterdiscord_version', None)


# noinspection PyTypeChecker
def dump_settings():
    try:
        settings = {
            'discord_installed_path': config.DISCORD_PARENT_PATH,
            'last_installed_discord_version': config.LAST_INSTALLED_DISCORD_VERSION,
            'disable_version_check': config.DISABLE_DISCORD_VERSION_CHECKING,
            'disable_bdai_autoupdate': config.DISABLE_BDAI_AUTOUPDATE,
            'last_installed_betterdiscord_version': config.LAST_INSTALLED_BETTERDISCORD_VERSION,
        }
        json.dump(settings, open(config.SETTINGS_PATH, 'w'), indent=2)
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
