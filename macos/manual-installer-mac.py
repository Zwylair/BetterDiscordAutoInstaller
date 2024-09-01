import os
import sys
import logging
import platform
import subprocess
import requests
import json
import time

# TODO: Need to refactor
# TODO: Need to add tests (no tests currently) -> Need to add missing error handling & edge cases


# setup loggers
logger = logging.getLogger(__name__)
logging.basicConfig(format="(%(asctime)s) %(message)s")
logger.setLevel(logging.INFO)

# BetterDiscord URL
BD_ASAR_URL = "https://github.com/rauenzi/BetterDiscordApp/releases/latest/download/betterdiscord.asar"

# MacOS-specific paths
HOME_DIR = os.path.expanduser("~")
BD_PARENT_PATH = os.path.join(HOME_DIR, "Library/Application Support/BetterDiscord")
DISCORD_PARENT_PATH = os.path.join(HOME_DIR, "Library/Application Support/discord")
DISCORD_EXECUTABLE_PATH = "/Applications/Discord.app"

BD_ASAR_SAVE_PATH = os.path.join(BD_PARENT_PATH, "data/betterdiscord.asar")


# load settings
CURRENT_SETTINGS_VERSION = 2
LAST_INSTALLED_DISCORD_VERSION = None


def get_path_for_current_discord_version(DISCORD_PARENT_PATH: str) -> str:
    # On MacOS, the discord version is set as a folder within Library/Application Support/discord --> ex. 0.0.315

    # gets all versions of discord installed
    discord_path = [
        i for i in os.listdir(DISCORD_PARENT_PATH) if i.replace(".", "").isdigit()
    ]
    discord_path.sort()
    latest_installed_discord_version = discord_path[-1]
    discord_path = os.path.join(DISCORD_PARENT_PATH, latest_installed_discord_version)
    return discord_path


def set_discord_index_js_path(discord_path: str) -> str:
    index_js_path = os.path.join(discord_path, "modules/discord_desktop_core/index.js")
    return index_js_path


def patch_discord_index_js(discord_index_js_path: str, bd_asar_save_path: str) -> None:
    # Open the index.js file
    logger.info("Attempting to patch Discord index file to use BetterDiscord...")
    with open(discord_index_js_path, "r+") as file:
        content = file.read()
        logger.info(f"Updating Discord index at: {discord_index_js_path}")
        if "betterdiscord.asar" not in content:
            # Insert the require line at the top
            content = f'require("{bd_asar_save_path}");\n' + content
            file.seek(0)
            file.write(content)
            file.truncate()
    logger.info("Patched Discord index file.")


def download_betterdiscord_asar(asar_url: str, bd_asar_save_path: str) -> None:
    logger.info("Downloading latest BetterDiscord asar file...")
    response = requests.get(asar_url)

    logger.info("Updating local BetterDiscord asar file with latest...")
    try:
        with open(bd_asar_save_path, "wb") as file:
            logger.info(f"Saving to: {bd_asar_save_path}")
            file.write(response.content)
    except Exception as e:
        logger.error(f"Error updating BetterDiscord asar file: {e}")

    logger.info("BetterDiscord asar file updated.")


def get_discord_version() -> str:
    info_plist_path = os.path.join(DISCORD_EXECUTABLE_PATH, "Contents/Info.plist")
    logger.info(f"Attempting to read Discord Info.plist at: {info_plist_path}")
    try:
        with open(info_plist_path, "r") as file:
            content = file.read()
            version = (
                content.split("<key>CFBundleShortVersionString</key>")[1]
                .split("<string>")[1]
                .split("</string>")[0]
            )
            logger.info(f"Discord version: {version}")
    except Exception as e:
        logger.error(f"Error reading Discord Info.plist: {e}")
        return "Unknown version"
    return version


def is_discord_shipit_process_running() -> bool:
    try:
        # List all processes with their parent process names
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        processes = result.stdout.splitlines()

        # Filter for processes named ShipIt with Discord as the parent process
        for process in processes:
            if "ShipIt" in process and "Discord" in process:
                return True
        return False
    except Exception as e:
        logger.error(f"Error checking ShipIt process: {e}")
        return False


def get_discord_update_dir() -> str:
    discord_cache_path = os.path.expanduser(
        "~/Library/Caches/com.hnc.Discord.ShipIt/ShipItState.plist"
    )
    logger.info(f"Reading Discord updater plist at: {discord_cache_path}")
    try:
        with open(discord_cache_path, "r") as file:
            content = file.read()
            plist_dict = json.loads(content)
            update_bundle_url = plist_dict.get("updateBundleURL", "")
            # Remove the 'file://' prefix if it exists and the "/Discord.app/"
            if update_bundle_url.startswith("file://"):
                update_bundle_url = update_bundle_url[7:-13]

            logger.info(f"Extracted updateBundleURL: {update_bundle_url}")
            return update_bundle_url

    except Exception as e:
        logger.error(f"Error reading Discord updater plist: {e}")
        return
    pass


# Waits 5 minutes for the Discord ShipIt (update) process to finish. Checks every 5 seconds.
def wait_for_discord_shipit(max_wait_time: int = 300, retry_interval: int = 5) -> bool:
    start_time = time.time()
    retries = 0
    max_retries = max_wait_time // retry_interval

    while is_discord_shipit_process_running():
        logger.info("Waiting for Discord ShipIt update process to finish...")
        logger.info(f"Retrying in {retry_interval} seconds...")
        time.sleep(retry_interval)

        # Check if we've exceeded the maximum retries or the max wait time
        retries += 1
        elapsed_time = time.time() - start_time

        if elapsed_time > max_wait_time or retries >= max_retries:
            logger.error(
                "Discord ShipIt process did not finish within the expected time. See if Discord is still updating. If so, wait until finished and try again."
            )
            return False

    logger.info("Discord ShipIt process finished successfully.")
    return True


# Waits 2 minutes for the Discord update process to empty Checks every 5 seconds.
def wait_for_discord_update_folder(
    update_directory: str, max_wait_time: int = 120, retry_interval: int = 5
) -> bool:
    start_time = time.time()
    retries = 0
    max_retries = max_wait_time // retry_interval

    while update_directory and os.path.exists(update_directory):
        logger.info(
            "Update directory found -> Discord update still in progress. Waiting for update folder to empty..."
        )
        logger.info(f"Retrying in {retry_interval} seconds...")
        time.sleep(retry_interval)

        # Check if we've exceeded the maximum retries or the max wait time
        retries += 1
        elapsed_time = time.time() - start_time

        if elapsed_time > max_wait_time or retries >= max_retries:
            logger.error(
                "Discord Update process did not finish within the expected time. See if Discord is still updating. If so, wait until finished and try again."
            )
            return False

    logger.info("Discord folder update process finished successfully.")
    return True


def discord_update_complete(update_directory: str) -> bool:
    if not wait_for_discord_shipit():
        logger.error(
            "Discord ShipIt still running. Make sure Discord has finished updating before running again."
        )
        return False

    if not wait_for_discord_update_folder(update_directory):
        logger.error(
            "Discord update folder still exists. Make sure Discord has finished updating before running again."
        )
        return False
    return True


def notify(title, text):
    os.system(f"""osascript -e 'display notification "{text}" with title "{title}"' """)


if __name__ == "__main__":

    notify("BetterDiscord Installer", "Script is starting...")
    # Makes sure it's MacOS
    if platform.system() != "Darwin":
        input(
            "Your system is not supported yet to using this script\n"
            "\n"
            "Press ENTER to exit."
        )
        sys.exit(1)

    logger.info("BetterDiscordAutoInstaller v1.2.0")
    logger.info(
        f""" Paths:
        HOME_DIR: {HOME_DIR}
        BD_PATH: {BD_PARENT_PATH}
        BD_ASAR_SAVE_PATH: {BD_ASAR_SAVE_PATH}
        DISCORD_PARENT_PATH: {DISCORD_PARENT_PATH}
        """
    )

    # Now do ^ when discord updates (trying to detect discord updates)

    discord_version_path = get_path_for_current_discord_version(DISCORD_PARENT_PATH)
    discord_index_js_path = set_discord_index_js_path(discord_version_path)
    discord_update_dir = get_discord_update_dir()

    if discord_update_complete(discord_update_dir):
        patch_discord_index_js(discord_index_js_path, BD_ASAR_SAVE_PATH)
        download_betterdiscord_asar(BD_ASAR_URL, BD_ASAR_SAVE_PATH)
        get_discord_version()
        notify("BetterDiscord Installer", "Installation complete!")

    else:
        print("Discord update not complete. Exiting...")
        notify("BetterDiscord Installer", "Discord update not complete. Exiting...")
        sys.exit(1)


