from funcs import *  # Import functions from funcs.py

def main():
    global DISCORD_PARENT_PATH, LAST_INSTALLED_DISCORD_VERSION, DISABLE_VERSION_CHECKING

    logger.info('BetterDiscordAutoInstaller v1.2.5\n')

    DISCORD_PARENT_PATH = find_discord_path()
    if not DISCORD_PARENT_PATH:
        logger.error("No valid Discord installation found.")
        DISCORD_PARENT_PATH = input("Enter the path to your Discord installation: ").strip()
        if not os.path.exists(DISCORD_PARENT_PATH):
            logger.error(f"Invalid path provided: {DISCORD_PARENT_PATH}")
            sys.exit(1)

    try:
        discord_core_folder = get_latest_installed_discord_folder_name(DISCORD_PARENT_PATH)
        discord_path = os.path.join(DISCORD_PARENT_PATH, discord_core_folder)
        LAST_INSTALLED_DISCORD_VERSION = discord_core_folder
        dump_settings()
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)

    logger.info("Killing any running Discord processes...")
    kill_discord()
    time.sleep(2)

    logger.info("Installing BetterDiscord...")
    install_betterdiscord(discord_path)

    PLUGIN_URLS = [
        'https://raw.githubusercontent.com/riolubruh/YABDP4Nitro/main/YABDP4Nitro.plugin.js',
        'https://mwittrien.github.io/BetterDiscordAddons/Plugins/PluginRepo/PluginRepo.plugin.js'
    ]
    PLUGIN_SAVE_PATHS = [
        os.path.join(APPDATA, 'BetterDiscord/plugins/YABDP4Nitro.plugin.js'),
        os.path.join(APPDATA, 'BetterDiscord/plugins/PluginRepo.plugin.js')
    ]

    install_plugins(PLUGIN_URLS, PLUGIN_SAVE_PATHS, APPDATA)

    logger.info("Restarting Discord...")
    start_discord(DISCORD_PARENT_PATH)

    logger.info("Installation complete. Exiting in 3 seconds...")
    time.sleep(3)
    sys.exit(0)

if __name__ == "__main__":
    main()
