import os
import subprocess
import psutil
import requests
import glob
import logging
import json
import re
import time
import sys

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='(%(asctime)s) %(message)s')

# Paths and Constants
SETTINGS_PATH = 'settings.json'
BD_ASAR_URL = 'https://github.com/rauenzi/BetterDiscordApp/releases/latest/download/betterdiscord.asar'
APPDATA = os.getenv('appdata')
LOCALAPPDATA = os.getenv('localappdata')
USERPROFILE = os.getenv('userprofile')

DISCORD_POSSIBLE_PATHS = [
    os.path.join(LOCALAPPDATA, 'Discord'),
    os.path.join(LOCALAPPDATA, 'DiscordPTB'),
    os.path.join(LOCALAPPDATA, 'DiscordCanary')
]

CURRENT_SETTINGS_VERSION: int
DISCORD_PARENT_PATH: str | None
LAST_INSTALLED_DISCORD_VERSION: str | None
DISABLE_VERSION_CHECKING: bool

def find_discord_path():
    global DISCORD_PARENT_PATH
    for path in DISCORD_POSSIBLE_PATHS:
        if os.path.exists(path):
            return path
    return None

def load_settings():
    global CURRENT_SETTINGS_VERSION, DISCORD_PARENT_PATH, \
        LAST_INSTALLED_DISCORD_VERSION, DISABLE_VERSION_CHECKING

    settings = json.load(open(SETTINGS_PATH)) if os.path.exists(SETTINGS_PATH) else {}
    CURRENT_SETTINGS_VERSION = settings.get('settings_version', 3)
    DISCORD_PARENT_PATH = settings.get('discord_installed_path', None)
    LAST_INSTALLED_DISCORD_VERSION = settings.get('last_installed_discord_version', None)
    DISABLE_VERSION_CHECKING = settings.get('disable_version_check', False)

def dump_settings():
    settings = {
        'settings_version': CURRENT_SETTINGS_VERSION,
        'discord_installed_path': DISCORD_PARENT_PATH,
        'last_installed_discord_version': LAST_INSTALLED_DISCORD_VERSION,
        'disable_version_check': DISABLE_VERSION_CHECKING,
    }
    json.dump(settings, open(SETTINGS_PATH, 'w'))

def download_plugin(url, save_path):
    """Downloads a plugin or library from the specified URL and saves it to the given path."""
    plugin_dir = os.path.dirname(save_path)
    if not os.path.exists(plugin_dir):
        os.makedirs(plugin_dir)  # Create the necessary directories

    if os.path.exists(save_path):
        logger.info(f"Plugin already exists at {save_path}. Skipping download.")
        return  # Skip download if the plugin already exists

    try:
        logger.info(f"Downloading from {url} to {save_path}...")
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as plugin_file:
                plugin_file.write(response.content)
            logger.info(f'Plugin or library downloaded and saved to {save_path}')
        else:
            logger.error(f"Failed to download plugin or library from {url}. HTTP status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while downloading the plugin or library: {e}")

def extract_dependencies_from_description(description):
    """Extracts and returns the dependencies from the plugin description, including libraries."""
    dependencies = []

    if 'depends on' in description.lower():
        start = description.lower().find('depends on') + len('depends on')
        end = description.find('\n', start)
        dependency_info = description[start:end].strip()
        
        if dependency_info:
            if not dependency_info.startswith("http"):
                dependency_info = f"https://{dependency_info}"
            dependencies.append(dependency_info)

    plugin_regex = r'https?://[^\s"]+\.plugin\.js'  
    found_plugins = re.findall(plugin_regex, description)

    if found_plugins:
        dependencies.extend(found_plugins)

    return dependencies

def check_and_download_dependencies(plugin_name, description, appdata):
    """Checks and downloads missing dependencies for a plugin by analyzing the description."""
    dependencies = extract_dependencies_from_description(description)
    
    for dependency_url in dependencies:
        if '${name}' in dependency_url:
            dependency_url = dependency_url.replace('${name}', plugin_name)
        
        dependency_name = dependency_url.split("/")[-1]
        
        # Check if the dependency is already installed
        if is_dependency_installed(dependency_name, appdata):
            logger.info(f"Dependency {dependency_name} for {plugin_name} is already installed. Skipping download.")
            continue  # Skip downloading this dependency if it's already installed
        
        dependency_path = os.path.join(appdata, 'BetterDiscord/plugins', dependency_name)
        
        logger.info(f"Downloading missing dependency: {dependency_name} for {plugin_name}...")
        download_plugin(dependency_url, dependency_path)

def is_plugin_installed(plugin_name, appdata):
    """Checks if the given plugin is already installed."""
    plugin_path = os.path.join(appdata, 'BetterDiscord/plugins', f"{plugin_name}.plugin.js")
    logger.info(f"Checking if plugin {plugin_name} is installed at {plugin_path}...")
    return os.path.exists(plugin_path)

def is_dependency_installed(dependency_name, appdata):
    """Checks if a given dependency is already installed."""
    dependency_path = os.path.join(appdata, 'BetterDiscord/plugins', f"{dependency_name}")
    logger.info(f"Checking if dependency {dependency_name} is installed at {dependency_path}...")
    return os.path.exists(dependency_path)

def install_plugins(plugin_urls, plugin_save_paths, appdata):
    """Handles plugin installation, including downloading and checking dependencies."""
    for url, path in zip(plugin_urls, plugin_save_paths):
        plugin_name = url.split("/")[-1].replace(".plugin.js", "")
        
        # Skip if the plugin is already installed
        if is_plugin_installed(plugin_name, appdata):
            logger.info(f"Plugin {plugin_name} is already installed. Skipping...")
            continue  # Skip this plugin and move to the next
        
        # Fetch the plugin description
        plugin_description = get_plugin_description(url)
        check_and_download_dependencies(plugin_name, plugin_description, appdata)  # Check and download dependencies

        # Download the plugin itself if not already installed
        logger.info(f'Downloading plugin from {url} to {path}...')
        download_plugin(url, path)

def get_plugin_description(url):
    """Fetches the description of a plugin (simulated in this case)."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            logger.error(f"Failed to fetch plugin description from {url}")
            return ""
    except requests.exceptions.RequestException as e:
        logger.error(f"Error retrieving plugin description: {e}")
        return ""

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

def install_betterdiscord(discord_path: str):
    appdata = os.getenv('appdata')
    bd_asar_path = os.path.join(appdata, 'BetterDiscord', 'data', 'betterdiscord.asar')

    os.makedirs(os.path.dirname(bd_asar_path), exist_ok=True)

    try:
        logger.info("Downloading BetterDiscord asar...")
        response = requests.get(BD_ASAR_URL)
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
    
    with open(index_js_path, 'rb') as f:
        content = f.readlines()

    bd_asar_path = bd_asar_path.replace("\\", "/")
    content.insert(0, f'require("{bd_asar_path}");\n'.encode())

    with open(index_js_path, 'wb') as f:
        f.writelines(content)
    
    logger.info(f"Patched {index_js_path} to include BetterDiscord.")
