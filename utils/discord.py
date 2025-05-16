import os
import logging
import subprocess

import psutil

import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="(%(asctime)s) %(message)s")


def get_discord_edition(discord_parent_path: str) -> str:
    for name in ("Canary", "PTB"):
        if f"Discord{name}" in discord_parent_path:
            return f"Discord{name}"
    return "Discord"


def get_log_file_path(discord_parent_path: str) -> str:
    edition = get_discord_edition(discord_parent_path)
    return f"{config.APPDATA}/{edition.lower()}/logs/{edition}_updater_rCURRENT.log"


def find_discord_path() -> str | None:
    for path in config.DISCORD_POSSIBLE_PATHS:
        if os.path.exists(path):
            return path
    return None


def get_latest_installed_discord_folder_name(discord_parent_path: str) -> str:
    if not os.path.exists(discord_parent_path):
        raise FileNotFoundError(f"Discord directory not found: {discord_parent_path}")

    discord_versions = [i for i in os.listdir(discord_parent_path) if i.startswith("app-")]
    if not discord_versions:
        raise FileNotFoundError(f"No 'app-*' folders found in: {discord_parent_path}")

    discord_versions.sort()
    return discord_versions[-1]


def kill_discord(discord_parent_path: str):
    executable_name = get_discord_edition(discord_parent_path) + ".exe"
    for process in psutil.process_iter(["name"]):
        if process.info["name"] == executable_name:
            try:
                logger.info(f"Killing process: {process.info["name"]} (PID: {process.pid})")
                process.kill()
            except psutil.NoSuchProcess:
                pass


def start_discord(discord_parent_path: str):
    logger.info(f"Starting Discord from {discord_parent_path}...")
    executable_name = get_discord_edition(discord_parent_path) + ".exe"

    update_exe = os.path.join(discord_parent_path, "Update.exe")
    if not os.path.exists(update_exe):
        raise FileNotFoundError(f"Update.exe not found in: {discord_parent_path}")

    command = f'"{update_exe}" --processStart {executable_name}'
    logger.info(f"Starting Discord using command: {command}")
    subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def is_discord_running(discord_parent_path: str) -> bool:
    executable_name = get_discord_edition(discord_parent_path) + ".exe"
    for process in psutil.process_iter(["name"]):
        if process.info.get("name") == executable_name:
            return True
    return False


def is_discord_updating(discord_parent_path: str) -> bool:
    update_finished_messages = ("Updater main thread exiting", "Already up to date. Nothing to do")

    try:
        with open(get_log_file_path(discord_parent_path), encoding="utf-8", errors="replace") as updater_log_file:
            content = updater_log_file.read()

        for message in update_finished_messages:
            if message in content:
                logger.info(f"Detected update end message: {message}")
                return False
        return True
    except PermissionError as e:
        logger.error("Cannot read log file.", exc_info=e)
        return False
    except FileNotFoundError as e:
        logger.error("Log file not found.", exc_info=e)
        return False
