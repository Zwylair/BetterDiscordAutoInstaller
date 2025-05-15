import os

APPDATA = os.getenv("appdata")
LOCALAPPDATA = os.getenv("localappdata")
USERPROFILE = os.getenv("userprofile")

BDAI_SCRIPT_VERSION = "1.4.0"
BDAI_LATEST_RELEASE_PAGE_URL = "https://github.com/Zwylair/BetterDiscordAutoInstaller/releases/latest"
BDAI_RAW_RELEASE_URL_TEMPLATE = "https://github.com/Zwylair/BetterDiscordAutoInstaller/archive/refs/tags/{tag}.zip"
BDAI_RELEASE_URL_TEMPLATE = "https://github.com/Zwylair/BetterDiscordAutoInstaller/releases/download/{tag}/BetterDiscordAutoInstaller-{tag}.zip"
SETTINGS_PATH = "settings.json" if "PYCHARM_HOSTED" in os.environ else "../settings.json"
GITHUB_TOKEN_FILE_PATH = "github_token" if "PYCHARM_HOSTED" in os.environ else "../github_token"

BD_LATEST_RELEASE_PAGE_URL = "https://github.com/rauenzi/BetterDiscordApp/releases/latest"
BD_ASAR_URL = "https://github.com/rauenzi/BetterDiscordApp/releases/latest/download/betterdiscord.asar"
BD_ASAR_PATH = os.path.join(APPDATA, "BetterDiscord", "data", "betterdiscord.asar")
BD_CI_ASAR_PATH = os.path.join(APPDATA, "BetterDiscord", "data", "betterdiscord-ci.asar")
BD_CI_WORKFLOWS_URL = "https://api.github.com/repos/BetterDiscord/BetterDiscord/actions/workflows/ci.yml/runs"

DISCORD_POSSIBLE_PATHS = [
    os.path.join(LOCALAPPDATA, "Discord"),
    os.path.join(LOCALAPPDATA, "DiscordPTB"),
    os.path.join(LOCALAPPDATA, "DiscordCanary")
]
