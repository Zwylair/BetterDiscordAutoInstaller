import os
import sys
import time
import logging
import subprocess
import urllib.request
import urllib.error
import psutil

try:
    import msvcrt
except ImportError:
    input(
        'Your system is not supported yet to using this script\n'
        '\n'
        'Press ENTER to exit.'
    )
    exit(1)

logger = logging.getLogger(__name__)
logging.basicConfig(format='(%(asctime)s) %(message)s')
logger.setLevel(logging.INFO)

APPDATA = os.getenv('appdata')
BD_ASAR_URL = 'https://github.com/rauenzi/BetterDiscordApp/releases/latest/download/betterdiscord.asar'
BD_ASAR_SAVE_PATH = os.path.join(APPDATA, 'BetterDiscord/data/betterdiscord.asar').replace('\\', '/')

DO_START_DISCORD: bool = '--do-not-start-discord' not in sys.argv
IS_STARTED_SILENTLY: bool = '--silent' in sys.argv

#

discord_parent_path = f'{os.getenv("localappdata")}/Discord/'
discord_path = [i for i in os.listdir(discord_parent_path) if i.startswith('app-')]  # remove all not 'app-' items
discord_path.sort()
discord_path = os.path.join(discord_parent_path, discord_path[-1])
discord_modules_path = os.path.join(discord_path, 'modules')
index_js_path = os.path.join(discord_modules_path, 'discord_desktop_core-1/discord_desktop_core/index.js')
bd_required_folders = [
    f'{APPDATA}/BetterDiscord',
    f'{APPDATA}/BetterDiscord/data',
    f'{APPDATA}/BetterDiscord/themes',
    f'{APPDATA}/BetterDiscord/plugins'
]

# making folders
logger.info('Making required folders...')

for folder in bd_required_folders:
    if not os.path.exists(folder):
        os.mkdir(folder)

logger.info('Folders have been made!')
print()
time.sleep(0.1)

# downloading betterdiscord asar
logger.info('Trying to download BetterDiscord asar file...')

while True:
    try:
        urllib.request.urlretrieve(BD_ASAR_URL, BD_ASAR_SAVE_PATH)
        break
    except urllib.error.HTTPError as err:
        logger.error('Timed out. Retrying to download in 2s...')
        time.sleep(2)

logger.info('Asar has been successfully downloaded!')
print()
time.sleep(0.1)

# patching index.js
logger.info('Trying to patch discord startup script...')

with open(index_js_path, 'rb') as file:
    content = file.readlines()

is_script_already_patched = [i for i in content if b'betterdiscord.asar' in i]  # leaves lines that have 'betterdiscord.asar' in it
is_script_already_patched = bool(len(is_script_already_patched))  # this line should be only once in the file

if is_script_already_patched:
    logger.info('Script already patched!')
else:
    content.insert(0, f'require("{BD_ASAR_SAVE_PATH}");\n'.encode())

    with open(index_js_path, 'wb') as file:
        file.writelines(content)

    logger.info('Patching finished!')
print()
time.sleep(0.1)


# restarting discord
if DO_START_DISCORD:
    logger.info('Trying restart discord...')

    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'Discord.exe':
            process.kill()

    os.chdir('c:/')
    subprocess.Popen(f'cmd /c start {os.path.join(discord_path, "discord.exe")}')
    logger.info('Discord has been restarted!')
print()
time.sleep(0.1)

logger.info('Installation finished!')

if not IS_STARTED_SILENTLY:
    logger.info('Press any key to exit...')
    msvcrt.getch()
