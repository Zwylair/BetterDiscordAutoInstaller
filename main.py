import time
from funcs import *  # Import functions
import funcs  # For editing the variables

def main():
    load_settings()

    logger.info(f'BetterDiscordAutoInstaller v{BDAI_SCRIPT_VERSION}')

    logger.info('Checking for BetterDiscordAutoInstaller updates...')
    if check_for_updates() and not funcs.DISABLE_BDAI_AUTOUPDATE:
        run_updater()

    logger.info("Retrieving Discord installation folder...")
    funcs.DISCORD_PARENT_PATH = find_discord_path()
    if not funcs.DISCORD_PARENT_PATH:
        logger.error("No valid Discord installation found.")

        funcs.DISCORD_PARENT_PATH = input("Enter the path to your Discord installation: ").strip()
        if not os.path.exists(funcs.DISCORD_PARENT_PATH):
            logger.error(f"Invalid path provided: {funcs.DISCORD_PARENT_PATH}")
            sys.exit(1)

    if not is_discord_running():
        logger.info("Discord is not running. Starting updater.")
        start_discord(funcs.DISCORD_PARENT_PATH)
        time.sleep(1)

        logger.info("Waiting for end of Discord updating.")
        while is_discord_updating(funcs.DISCORD_PARENT_PATH):
            time.sleep(0.5)

    discord_core_folder = get_latest_installed_discord_folder_name(funcs.DISCORD_PARENT_PATH)
    discord_path = os.path.join(funcs.DISCORD_PARENT_PATH, discord_core_folder)
    is_discord_up_to_date = discord_core_folder == funcs.LAST_INSTALLED_DISCORD_VERSION and not funcs.DISABLE_DISCORD_VERSION_CHECKING

    if is_discord_up_to_date:
        logger.info("Discord is up to date.")
    else:
        funcs.LAST_INSTALLED_DISCORD_VERSION = discord_core_folder
        dump_settings()

    is_betterdiscord_up_to_date = not check_for_betterdiscord_updates()
    if not is_discord_up_to_date or not is_betterdiscord_up_to_date:
        if not is_discord_up_to_date:
            logger.info("Discord was updated.")

        if not is_betterdiscord_up_to_date:
            logger.info("Found an available update for BetterDiscord.")

        logger.info("Killing any running Discord processes...")
        kill_discord()
        time.sleep(2)

        logger.info("Installing BetterDiscord...")
        install_betterdiscord(discord_path)

        PLUGIN_URLS = [
            'https://raw.githubusercontent.com/riolubruh/YABDP4Nitro/main/YABDP4Nitro.plugin.js'
        ]
        PLUGIN_SAVE_PATHS = [
            os.path.join(APPDATA, 'BetterDiscord/plugins/YABDP4Nitro.plugin.js')
        ]

        install_plugins(PLUGIN_URLS, PLUGIN_SAVE_PATHS, APPDATA)

        logger.info("Restarting Discord...")
        start_discord(funcs.DISCORD_PARENT_PATH)
    else:
        logger.info("BetterDiscord is up to date.")

    logger.info("Installation complete. Exiting in 3 seconds...")
    time.sleep(3)
    sys.exit(0)

if __name__ == "__main__":
    main()
