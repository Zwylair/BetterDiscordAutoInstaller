import os
import logging
import subprocess

import psutil

import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='(%(asctime)s) %(message)s')


def find_discord_path() -> str | None:
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
        executable_name = "Discord.exe"

    update_exe = os.path.join(discord_parent_path, "Update.exe")
    if not os.path.exists(update_exe):
        raise FileNotFoundError(f"Update.exe not found in: {discord_parent_path}")

    command = f'"{update_exe}" --processStart {executable_name}'
    logger.info(f"Starting Discord using command: {command}")
    subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


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
