import os
import sys
import time
import logging
import platform
import subprocess
import psutil
import requests

if platform.system() != 'Windows':
    input(
        'Your system is not supported yet to using this script\n'
        '\n'
        'Press ENTER to exit.'
    )
    sys.exit(1)

logger = logging.getLogger(__name__)
logging.basicConfig(format='(%(asctime)s) %(message)s')
logger.setLevel(logging.INFO)

APPDATA = os.getenv('appdata')
LOCALAPPDATA = os.getenv('localappdata')
BD_ASAR_URL = 'https://github.com/rauenzi/BetterDiscordApp/releases/latest/download/betterdiscord.asar'
BD_ASAR_SAVE_PATH = os.path.join(APPDATA, 'BetterDiscord/data/betterdiscord.asar').replace('\\', '/')

#
logger.info('Killing discord...')

# killing discord to prevent any errors
for process in psutil.process_iter(['name']):
    if process.info['name'] == 'Discord.exe':
        process.kill()

# installing the latest version of discord (waiting for update.exe closing)
logger.info('Updating discord to latest version...')

subprocess.Popen(f'{os.path.join(LOCALAPPDATA, "Discord/Update.exe")} --processStart Discord.exe --process-start-args --start-minimized')
quit_from_loop = False

while True:
    for process in psutil.process_iter(['pid', 'name']):
        if process.name() == 'gpu_encoder_helper.exe':
            while True:
                try:
                    process.status()  # idle request which causes error when closed
                    time.sleep(1)
                except psutil.NoSuchProcess:
                    quit_from_loop = True
                    break

    time.sleep(0.5)

    if quit_from_loop:
        break

for process in psutil.process_iter(['name']):
    if process.info['name'] == 'Discord.exe':
        try:
            process.kill()
        except psutil.NoSuchProcess:
            pass


logger.info('Update finished. Patching...')
print()
time.sleep(0.1)

# patching

# determining the latest installed version of discord
discord_parent_path = f'{LOCALAPPDATA}/Discord/'
discord_path = [i for i in os.listdir(discord_parent_path) if i.startswith('app-')]  # remove all not 'app-' items
discord_path.sort()  # the oldest version will be the last of list
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
        os.makedirs(folder)

logger.info('Folders have been made!')
print()
time.sleep(0.1)

# downloading betterdiscord asar
logger.info('Trying to download BetterDiscord asar file...')

while True:
    response = requests.get(BD_ASAR_URL)

    if response.status_code == 200:
        with open(BD_ASAR_SAVE_PATH, 'wb') as file:
            file.write(response.content)
        break
    else:
        logger.info(f'Failed to download asar ({response.status_code}). Retrying in 3 seconds...')
        time.sleep(3)

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
logger.info('Trying restart discord...')

for process in psutil.process_iter(['name']):
    if process.info['name'] == 'Discord.exe':
        process.kill()

time.sleep(1)

# running discord from c:/ for prevent locking the script's working dir
script_env_path = os.path.dirname(os.path.abspath(__file__))
os.chdir('c:/')

subprocess.Popen(f'cmd /c start {os.path.join(discord_path, "discord.exe")}')
os.chdir(script_env_path)


logger.info('Discord has been restarted!')
print()
time.sleep(0.1)

logger.info('Installation finished!')
logger.info('Exiting in 3 seconds...')
time.sleep(3)
sys.exit(0)
