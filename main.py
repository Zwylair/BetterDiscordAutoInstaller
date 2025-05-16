import os
import sys
import time
import logging

import utils
import config
import plugins

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="(%(asctime)s) %(message)s")


def main():
    config.load_settings()
    config.load_github_token()

    logger.info(f"BetterDiscordAutoInstaller v{config.BDAI_SCRIPT_VERSION}")

    logger.info("Checking for BetterDiscordAutoInstaller updates...")
    if utils.check_for_bdai_updates() and not config.DISABLE_BDAI_AUTOUPDATE:
        utils.run_updater()

    logger.info("Retrieving Discord installation folder...")
    if not config.DISCORD_PARENT_PATH:
        config.DISCORD_PARENT_PATH = utils.find_discord_path()

        if not config.DISCORD_PARENT_PATH:
            logger.error("No valid Discord installation found.")

            config.DISCORD_PARENT_PATH = input("Enter the path to your Discord installation: ").strip()
            if not os.path.exists(config.DISCORD_PARENT_PATH):
                logger.error(f"Invalid path provided: {config.DISCORD_PARENT_PATH}")
                sys.exit(1)
    logger.info(f"Processing Discord installation: {config.DISCORD_PARENT_PATH}")
    logger.info("")

    if not utils.is_discord_running(config.DISCORD_PARENT_PATH):
        # wipe logs, because discord doesn't do that after every updater run
        with open(utils.get_log_file_path(config.DISCORD_PARENT_PATH), "w") as f:
            f.write("")

        logger.info("Discord is not running. Starting updater.")
        utils.start_discord(config.DISCORD_PARENT_PATH)
        time.sleep(1)

        logger.info("Waiting for end of Discord updating.")
        while utils.is_discord_updating(config.DISCORD_PARENT_PATH):
            time.sleep(0.5)

    discord_core_folder = utils.get_latest_installed_discord_folder_name(config.DISCORD_PARENT_PATH)
    discord_path = os.path.join(config.DISCORD_PARENT_PATH, discord_core_folder)
    bd_release_tag = utils.get_release_tag(config.USE_BD_CI_RELEASES)

    is_last_patch_is_up_to_date = discord_core_folder == config.LAST_INSTALLED_DISCORD_VERSION and not config.DISABLE_DISCORD_VERSION_CHECKING
    is_bd_injected_already = utils.is_bd_injected(discord_path, config.USE_BD_CI_RELEASES)
    bd_has_updates = utils.check_for_bd_updates(config.USE_BD_CI_RELEASES)
    force_update_flag = "--force" in sys.argv

    logger.info("")

    if (
            not is_last_patch_is_up_to_date
            or not is_bd_injected_already
            or bd_has_updates
            or force_update_flag
    ):
        logger.info("Killing any running Discord processes...")
        utils.kill_discord(discord_path)
        time.sleep(2)

        logger.info("")

        if force_update_flag:
            logger.info("Force-set update flags.")
            is_last_patch_is_up_to_date = False
            bd_has_updates = True

        if not is_last_patch_is_up_to_date:
            logger.info("Discord was updated. Verifying injection patch...")
            config.LAST_INSTALLED_DISCORD_VERSION = discord_core_folder
            config.dump_settings()
            is_bd_injected_already = False

        if not is_bd_injected_already:
            logger.info(f"Verifying BetterDiscord {bd_release_tag} injection patch.")
            utils.inject_patch(discord_path, config.USE_BD_CI_RELEASES)

        if bd_has_updates:
            logger.info(f"BetterDiscord {bd_release_tag} has a new version, updating asar only.")
            utils.update_bd_asar_only(config.USE_BD_CI_RELEASES)

        logger.info("")
        logger.info("Restarting Discord...")
        utils.start_discord(config.DISCORD_PARENT_PATH)

        plugins_list = [
            plugins.PluginInfo.from_url("https://raw.githubusercontent.com/riolubruh/YABDP4Nitro/main/YABDP4Nitro.plugin.js")
        ]

        logger.info("")
        for plugin_info in plugins_list:
            logger.info(f"Installing {plugin_info.get_name()} plugin...")
            plugins.download_plugin(plugin_info)
    else:
        logger.info(f"BetterDiscord {bd_release_tag} is up to date and injected. No action needed.")

    logger.info("")
    logger.info("Installation complete. Exiting in 3 seconds...")
    time.sleep(3)
    sys.exit(0)


if __name__ == "__main__":
    main()
