import os
import subprocess
import psutil


def start_discord(discord_parent_path: str):
    # running discord from c:/ for prevent locking the script's working dir
    script_working_dir = os.getcwd()

    os.chdir('c:/')
    subprocess.Popen(f'{os.path.join(discord_parent_path, "Update.exe")} --processStart Discord.exe')
    os.chdir(script_working_dir)


def get_discord_state() -> tuple[bool, bool]:
    is_discord_running = False
    is_discord_updating = True

    # The "--service-sandbox-type=audio" argument will only be in the
    # updated discord instance, so it won't be in the update module

    for process in psutil.process_iter(['name']):
        if process.info.get('name') == 'Discord.exe':
            is_discord_running = True

            try:
                for arg in process.cmdline():
                    if '--service-sandbox-type=audio' in arg:
                        is_discord_updating = False
            except psutil.NoSuchProcess:
                pass

    return is_discord_running, is_discord_updating


def kill_discord():
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'Discord.exe':
            try:
                process.kill()
            except psutil.NoSuchProcess:
                pass


def get_latest_installed_discord_folder_name(discord_parent_path: str) -> str:
    discord_path = [i for i in os.listdir(discord_parent_path) if i.startswith('app-')]  # remove all not 'app-' items
    discord_path.sort()
    latest_installed_discord_version = discord_path[-1]  # the oldest version will be the last of list
    return latest_installed_discord_version
