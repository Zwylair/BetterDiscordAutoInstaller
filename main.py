import sys
import time
import json
import glob
import shutil
import logging
import requests
import os
import subprocess

from funcs import *


def dump_settings():
    json.dump(
        {
            'settings_version': CURRENT_SETTINGS_VERSION,
            'discord_installed_path': DISCORD_PARENT_PATH,
            'last_installed_discord_version': LAST_INSTALLED_DISCORD_VERSION,
            'disable_version_check': DISABLE_VERSION_CHECKING,
        },
        open(SETTINGS_PATH, 'w')
    )


if os.name != 'nt':
    input(
        'Your system is not supported to use this script\n'
        '\n'
        'Press ENTER to exit.'
    )
    sys.exit(0)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='(%(asctime)s) %(message)s')
appdata = os.getenv('appdata')
home = os.getenv('userprofile')
localappdata = os.getenv('localappdata')

SETTINGS_PATH = 'settings.json'
BD_ASAR_URL = 'https://github.com/rauenzi/BetterDiscordApp/releases/latest/download/betterdiscord.asar'
BD_ASAR_SAVE_PATH = os.path.join(appdata, 'BetterDiscord/data/betterdiscord.asar').replace('\\', '/')

logger.info('BetterDiscordAutoInstaller v1.2.3\n')

# default settings
CURRENT_SETTINGS_VERSION = 3
DISCORD_PARENT_PATH = f'{localappdata}\\Discord'
DISCORD_PTB_PATH = f'{localappdata}\\DiscordPTB'
DISCORD_CANARY_PATH = f'{localappdata}\\DiscordCanary'
LAST_INSTALLED_DISCORD_VERSION = None
DISABLE_VERSION_CHECKING = False

if shutil.which('scoop') is not None:
    scoop_info = subprocess.run(['scoop', 'list', 'discord'], capture_output=True, text=True, shell=True).stdout.splitlines()
    discord_line = next((line for line in scoop_info if line.startswith('discord')), None)
    if discord_line and not glob.glob(f'{home}\\scoop\\apps\\discord*\\current\\discord-portable.exe'):
        scoop_apps = os.listdir(f'{home}\\scoop\\apps')
        for app in scoop_apps:
            if app.startswith('discord'):
                DISCORD_PARENT_PATH = f'{home}\\scoop\\apps\\{app}\\current'
                break

# try to load settings
if os.path.exists(SETTINGS_PATH):
    try:
        settings = json.load(open(SETTINGS_PATH))
    except json.JSONDecodeError:
        logger.info('The settings have been corrupted. Using default values.')
    else:
        settings_version = settings.get('settings_version', CURRENT_SETTINGS_VERSION)
        DISCORD_PARENT_PATH = settings.get('discord_installed_path', DISCORD_PARENT_PATH)
        LAST_INSTALLED_DISCORD_VERSION = settings.get('last_installed_discord_version', LAST_INSTALLED_DISCORD_VERSION)
        DISABLE_VERSION_CHECKING = settings.get('disable_version_check', DISABLE_VERSION_CHECKING)

latest_installed_discord_version = get_latest_installed_discord_folder_name(DISCORD_PARENT_PATH)
discord_path = os.path.join(DISCORD_PARENT_PATH, latest_installed_discord_version)

# get discord location from user if it is invalid
while True:
    if not os.path.exists(os.path.join(DISCORD_PARENT_PATH, 'Update.exe')) and not os.path.exists(os.path.join(discord_path, 'Discord.exe')):
        if os.path.exists(os.path.join(DISCORD_PTB_PATH, 'Update.exe')):
            DISCORD_PARENT_PATH = DISCORD_PTB_PATH
        elif os.path.exists(os.path.join(DISCORD_CANARY_PATH, 'Update.exe')):
            DISCORD_PARENT_PATH = DISCORD_CANARY_PATH
        else:
            logger.info(f'Discord was not found at "{DISCORD_PARENT_PATH}".\nEnter the path to folder with "Update.exe" for normal installations or full path of ~\\scoop\\apps\\discord\\current\\app for scoop installations')
            DISCORD_PARENT_PATH = input('\n=> ')
            dump_settings()
    else:
        break

is_discord_running, is_discord_updating = get_discord_state()

if is_discord_running and not is_discord_updating:
    if not DISABLE_VERSION_CHECKING and latest_installed_discord_version == LAST_INSTALLED_DISCORD_VERSION:
        logger.info('Discord is up-to-date, no patch required. Exit in 3 seconds...')
        time.sleep(3)
        sys.exit(0)

    logger.info('Discord is running and not updating. Killing discord...')
    kill_discord()
    time.sleep(2)  # discord may not close instantly, so we need to wait for a while
    is_discord_running = False

# wait for discord updater close and check versions
if is_discord_running and is_discord_updating:
    if not DISABLE_VERSION_CHECKING:
        logger.info('Discord updater is running. Waiting for the updater to finish...')

        while True:
            is_discord_running, is_discord_updating = get_discord_state()

            if is_discord_running and not is_discord_updating:
                break

# installing the latest version of discord
if not is_discord_running:
    start_discord(DISCORD_PARENT_PATH)
    logger.info('Discord updater has been started.')
    logger.info('Waiting for the updater to finish...')

    while True:
        is_discord_running, is_discord_updating = get_discord_state()
        if is_discord_running and not is_discord_updating:
            break

logger.info('The update has been completed.\n')

# patching
latest_installed_discord_version = get_latest_installed_discord_folder_name(DISCORD_PARENT_PATH)
discord_path = os.path.join(DISCORD_PARENT_PATH, latest_installed_discord_version)
LAST_INSTALLED_DISCORD_VERSION = latest_installed_discord_version
dump_settings()

kill_discord()
time.sleep(2)

# making folders
logger.info('Creating folders...')

bd_required_folders = [
    os.path.join(appdata, 'BetterDiscord'),
    os.path.join(appdata, 'BetterDiscord/data'),
    os.path.join(appdata, 'BetterDiscord/themes'),
    os.path.join(appdata, 'BetterDiscord/plugins')
]

for folder in bd_required_folders:
    os.makedirs(folder, exist_ok=True)

logger.info('Folders have been created.\n')

# downloading betterdiscord asar
logger.info('Trying to download BetterDiscord asar...')

while True:
    try:
        response = requests.get(BD_ASAR_URL)
    except requests.exceptions.ConnectionError:
        logger.info('Failed to download asar. Retrying in 3 seconds...')
        time.sleep(3)
    else:
        with open(BD_ASAR_SAVE_PATH, 'wb') as file:
            file.write(response.content)
        break

logger.info('Asar has been successfully downloaded.\n')

# patching index.js
logger.info('Trying to patch discord launch script...')

index_js_path = os.path.join(discord_path, 'modules/discord_desktop_core-1/discord_desktop_core/index.js')

with open(index_js_path, 'rb') as file:
    content = file.readlines()

is_script_already_patched = [i for i in content if b'betterdiscord.asar' in i]  # leaves lines that have 'betterdiscord.asar' in it
is_script_already_patched = bool(len(is_script_already_patched))  # this line should be only once in the file

if is_script_already_patched:
    logger.info('The launch script has already been patched.\n')
else:
    content.insert(0, f'require("{BD_ASAR_SAVE_PATH}");\n'.encode())
    with open(index_js_path, 'wb') as file:
        file.writelines(content)

    logger.info('The launch script has been successfully patched.\n')

start_discord(DISCORD_PARENT_PATH)
logger.info('Discord has been started.\n')

logger.info('Installation finished.')
logger.info('Exiting in 3 seconds...')
time.sleep(3)
sys.exit(0)
