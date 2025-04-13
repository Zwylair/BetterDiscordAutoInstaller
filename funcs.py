import os
import sys
import glob
import logging
import subprocess

import psutil
import requests

import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='(%(asctime)s) %(message)s')


def find_discord_path():
    for path in config.DISCORD_POSSIBLE_PATHS:
        if os.path.exists(path):
            return path
    return None

def get_latest_installed_discord_folder_name(discord_parent_path: str) -> str:
    if not os.path.exists(discord_parent_path):
        raise FileNotFoundError(f"Discord directory not found: {discord_parent_path}")
    
    discord_versions = [i for i in os.listdir(discord_parent_path) if i.startswith('app-')]
    if not discord_versions:
        raise FileNotFoundError(f"No 'app-*' folders found in: {discord_parent_path}")
    
    discord_versions.sort()
    return discord_versions[-1]

def kill_discord():
    for process in psutil.process_iter(['name']):
        if process.info['name'] in ['Discord.exe', 'DiscordPTB.exe', 'DiscordCanary.exe']:
            try:
                logger.info(f"Killing process: {process.info['name']} (PID: {process.pid})")
                process.kill()
            except psutil.NoSuchProcess:
                pass

def start_discord(discord_parent_path: str):
    logger.info(f"Starting Discord from {discord_parent_path}...")
    
    if "DiscordCanary" in discord_parent_path:
        executable_name = "DiscordCanary.exe"
    elif "DiscordPTB" in discord_parent_path:
        executable_name = "DiscordPTB.exe"
    else:
        executable_name = "Discord.exe"  # Default to stable Discord

    update_exe = os.path.join(discord_parent_path, "Update.exe")
    if not os.path.exists(update_exe):
        raise FileNotFoundError(f"Update.exe not found in: {discord_parent_path}")

    command = f'"{update_exe}" --processStart {executable_name}'
    logger.info(f"Starting Discord using command: {command}")
    subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def is_betterdiscord_injected(discord_path: str) -> bool:
    appdata = os.getenv('appdata')
    bd_asar_path = os.path.join(appdata, 'BetterDiscord', 'data', 'betterdiscord.asar')
    bd_asar_path_normalized = bd_asar_path.replace("\\", "/")

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

def check_for_updates() -> bool:
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

def fetch_latest_betterdiscord_release() -> str:
    latest_release_url = requests.head(config.BD_LATEST_RELEASE_PAGE_URL, allow_redirects=True)
    return latest_release_url.url.split('/')[-1]

def check_for_betterdiscord_updates() -> bool:
    """Checks for updates and return True if there is an available update, False otherwise"""
    return fetch_latest_betterdiscord_release() != config.LAST_INSTALLED_BETTERDISCORD_VERSION

def is_discord_running() -> bool:
    for process in psutil.process_iter(['name']):
        if process.info.get('name') in ['Discord.exe', 'DiscordPTB.exe', 'DiscordCanary.exe']:
            return True
    return False

def is_discord_updating(discord_parent_path: str) -> bool:
    try:
        with open(os.path.join(discord_parent_path, "Discord_updater_rCURRENT.log")) as updater_log_file:
            return "Updater main thread exiting" not in updater_log_file.readlines()[-1]
    except FileNotFoundError:
        return False
