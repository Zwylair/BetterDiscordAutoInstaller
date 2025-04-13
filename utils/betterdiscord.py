import os
import glob
import logging

import requests

import config
from utils.other import backslash_path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='(%(asctime)s) %(message)s')


def is_betterdiscord_injected(discord_path: str) -> bool:
    appdata = os.getenv('appdata')
    bd_asar_path_normalized = backslash_path(os.path.join(appdata, 'BetterDiscord', 'data', 'betterdiscord.asar'))
    core_path_pattern = os.path.join(discord_path, 'modules/discord_desktop_core-*/discord_desktop_core')
    core_paths = glob.glob(core_path_pattern)

    if not core_paths:
        logger.warning("Discord core path not found when checking BetterDiscord injection.")
        return False

    index_js_path = os.path.join(core_paths[0], 'index.js')
    if not os.path.exists(index_js_path):
        logger.warning("Discord index.js not found.")
        return False

    with open(index_js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return f'require("{bd_asar_path_normalized}");' in content


def update_betterdiscord_asar_only():
    appdata = os.getenv('appdata')
    bd_asar_path = os.path.join(appdata, 'BetterDiscord', 'data', 'betterdiscord.asar')

    os.makedirs(os.path.dirname(bd_asar_path), exist_ok=True)

    try:
        logger.info("Downloading BetterDiscord asar...")
        response = requests.get(config.BD_ASAR_URL)
        with open(bd_asar_path, 'wb') as f:
            f.write(response.content)
        logger.info("BetterDiscord asar downloaded successfully.")

    except requests.exceptions.ConnectionError:
        logger.error("Failed to download BetterDiscord asar.")

    config.LAST_INSTALLED_BETTERDISCORD_VERSION = fetch_latest_betterdiscord_release()
    config.dump_settings()


def install_betterdiscord(discord_path: str):
    appdata = os.getenv('appdata')
    bd_asar_path = os.path.join(appdata, 'BetterDiscord', 'data', 'betterdiscord.asar')

    os.makedirs(os.path.dirname(bd_asar_path), exist_ok=True)

    try:
        logger.info("Downloading BetterDiscord asar...")
        response = requests.get(config.BD_ASAR_URL)
        with open(bd_asar_path, 'wb') as f:
            f.write(response.content)
        logger.info("BetterDiscord asar downloaded successfully.")
    except requests.exceptions.ConnectionError:
        logger.error("Failed to download BetterDiscord asar.")
        return

    core_path_pattern = os.path.join(discord_path, 'modules/discord_desktop_core-*/discord_desktop_core')
    core_paths = glob.glob(core_path_pattern)

    if not core_paths:
        raise FileNotFoundError(f"No matching discord_desktop_core-* folder found in: {discord_path}")

    index_js_path = os.path.join(core_paths[0], 'index.js')

    with open(index_js_path, 'r', encoding='utf-8') as f:
        content = f.readlines()

    bd_asar_path = bd_asar_path.replace("\\", "/")
    require_line = f'require("{bd_asar_path}");\n'

    if any(require_line.strip() in line for line in content):
        logger.info("BetterDiscord is already injected. Skipping patch.")
        return

    content.insert(0, require_line)

    with open(index_js_path, 'w', encoding='utf-8') as f:
        f.writelines(content)

    config.LAST_INSTALLED_BETTERDISCORD_VERSION = fetch_latest_betterdiscord_release()
    config.dump_settings()

    logger.info(f"Patched {index_js_path} to include BetterDiscord.")


def fetch_latest_betterdiscord_release() -> str:
    latest_release_url = requests.head(config.BD_LATEST_RELEASE_PAGE_URL, allow_redirects=True)
    return latest_release_url.url.split('/')[-1]


def check_for_betterdiscord_updates() -> bool:
    """Checks for updates and return True if there is an available update, False otherwise"""
    return fetch_latest_betterdiscord_release() != config.LAST_INSTALLED_BETTERDISCORD_VERSION
