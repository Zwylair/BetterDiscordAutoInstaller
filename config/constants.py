import os

BDAI_SCRIPT_VERSION = '1.3.3'
BDAI_LATEST_RELEASE_PAGE_URL = 'https://github.com/Zwylair/BetterDiscordAutoInstaller/releases/latest'
BD_LATEST_RELEASE_PAGE_URL = 'https://github.com/rauenzi/BetterDiscordApp/releases/latest'
BDAI_RAW_RELEASE_URL_TEMPLATE = 'https://github.com/Zwylair/BetterDiscordAutoInstaller/archive/refs/tags/{tag}.zip'
BDAI_RELEASE_URL_TEMPLATE = 'https://github.com/Zwylair/BetterDiscordAutoInstaller/releases/download/{tag}/BetterDiscordAutoInstaller-{tag}.zip'
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

DISCORD_PARENT_PATH: str | None
LAST_INSTALLED_DISCORD_VERSION: str | None
DISABLE_DISCORD_VERSION_CHECKING: bool
DISABLE_BDAI_AUTOUPDATE: bool
LAST_INSTALLED_BETTERDISCORD_VERSION: str | None
