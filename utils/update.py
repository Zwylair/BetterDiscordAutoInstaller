import sys
import logging
import subprocess

import requests

import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='(%(asctime)s) %(message)s')


def check_for_bdai_updates() -> bool:
    """Checks for updates and return True if there is an available update, False otherwise"""

    latest_release_url = requests.head(config.BDAI_LATEST_RELEASE_PAGE_URL, allow_redirects=True)
    latest_available_version = latest_release_url.url.split('/')[-1].lstrip('v')

    if config.BDAI_SCRIPT_VERSION != latest_available_version:
        logger.info(f'A new version available ({config.BDAI_SCRIPT_VERSION} -> {latest_available_version}).')

        if config.DISABLE_BDAI_AUTOUPDATE:
            logger.info(f'To update, go to {config.BDAI_LATEST_RELEASE_PAGE_URL}\n')
        return True
    else:
        logger.info('BetterDiscordAutoInstaller is up to date.\n')
        return False


def run_updater():
    logger.info('Running updater...')

    updater_run_command = ['updater.exe'] if getattr(sys, 'frozen', False) else [sys.executable, 'updater.py']
    subprocess.run(updater_run_command)
