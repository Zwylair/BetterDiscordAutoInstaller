import time
from funcs import *  # Import functions
import funcs  # For editing the variables

def main():
    config.load_settings()

    logger.info(f'BetterDiscordAutoInstaller v{config.BDAI_SCRIPT_VERSION}')

    logger.info('Checking for BetterDiscordAutoInstaller updates...')
    if check_for_updates() and not config.DISABLE_BDAI_AUTOUPDATE:
        run_updater()

    logger.info("Retrieving Discord installation folder...")
    config.DISCORD_PARENT_PATH = find_discord_path()
    if not config.DISCORD_PARENT_PATH:
        logger.error("No valid Discord installation found.")

        config.DISCORD_PARENT_PATH = input("Enter the path to your Discord installation: ").strip()
        if not os.path.exists(config.DISCORD_PARENT_PATH):
            logger.error(f"Invalid path provided: {config.DISCORD_PARENT_PATH}")
            sys.exit(1)

    if not is_discord_running():
        logger.info("Discord is not running. Starting updater.")
        start_discord(config.DISCORD_PARENT_PATH)
        time.sleep(1)

        logger.info("Waiting for end of Discord updating.")
        while is_discord_updating(config.DISCORD_PARENT_PATH):
            time.sleep(0.5)

    discord_core_folder = get_latest_installed_discord_folder_name(config.DISCORD_PARENT_PATH)
    discord_path = os.path.join(config.DISCORD_PARENT_PATH, discord_core_folder)
    is_discord_up_to_date = discord_core_folder == config.LAST_INSTALLED_DISCORD_VERSION and not config.DISABLE_DISCORD_VERSION_CHECKING

    if is_discord_up_to_date:
        logger.info("Discord is up to date.")
    else:
        funcs.LAST_INSTALLED_DISCORD_VERSION = discord_core_folder
        config.dump_settings()

    is_betterdiscord_up_to_date = not check_for_betterdiscord_updates()
    is_betterdiscord_injected_already = is_betterdiscord_injected(discord_path)

    if not is_discord_up_to_date or not is_betterdiscord_injected_already:
        if not is_discord_up_to_date:
            logger.info("Discord was updated.")
        if not is_betterdiscord_injected_already:
            logger.info("BetterDiscord is not injected. Proceeding with patch.")

        logger.info("Killing any running Discord processes...")
        kill_discord()
        time.sleep(2)

        logger.info("Installing BetterDiscord...")
        install_betterdiscord(discord_path)

        logger.info("Restarting Discord...")
        start_discord(config.DISCORD_PARENT_PATH)

        PLUGIN_URLS = [
            'https://raw.githubusercontent.com/riolubruh/YABDP4Nitro/main/YABDP4Nitro.plugin.js'
        ]
        PLUGIN_SAVE_PATHS = [
            os.path.join(config.APPDATA, 'BetterDiscord/plugins/YABDP4Nitro.plugin.js')
        ]

        install_plugins(PLUGIN_URLS, PLUGIN_SAVE_PATHS, config.APPDATA)

    elif not is_betterdiscord_up_to_date:
        logger.info("Killing any running Discord processes...")
        kill_discord()
        time.sleep(2)
        logger.info("BetterDiscord has a new version, updating asar only.")
        update_betterdiscord_asar_only()
        logger.info("Restarting Discord...")
        start_discord(config.DISCORD_PARENT_PATH)
    else:
        logger.info("BetterDiscord is up to date and injected. No action needed.")

    logger.info("Installation complete. Exiting in 3 seconds...")

    time.sleep(3)
    sys.exit(0)

if __name__ == "__main__":
    main()
