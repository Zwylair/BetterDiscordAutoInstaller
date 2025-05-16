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

    all_discord_paths = {
        config.DiscordEdition.STABLE: config.DISCORD_PARENT_PATH,
        config.DiscordEdition.CANARY: config.DISCORD_CANARY_PARENT_PATH,
        config.DiscordEdition.PTB: config.DISCORD_PTB_PARENT_PATH
    }

    for edition, discord_parent_path in all_discord_paths.items():
        logger.info(f"Retrieving {edition} installation folder...")

        if discord_parent_path:
            break
    else:
        logger.error("No any valid Discord installation found.")
        logger.info("Enter the path to your Discord Stable installation")

        config.DISCORD_PARENT_PATH = input(">>> ").strip()
        if not os.path.exists(config.DISCORD_PARENT_PATH):
            logger.error(f"Invalid path provided: {config.DISCORD_PARENT_PATH}")
            sys.exit(1)

        all_discord_paths[config.DiscordEdition.STABLE] = config.DISCORD_PARENT_PATH
        config.dump_settings()

    bd_release_tag = utils.get_release_tag(config.USE_BD_CI_RELEASES)
    bd_has_updates = utils.check_for_bd_updates(config.USE_BD_CI_RELEASES)
    force_update_flag = "--force" in sys.argv

    for discord_edition, discord_parent_path in all_discord_paths.items():
        if not discord_parent_path:
            continue

        logger.info("")
        logger.info(f"Processing {discord_edition} installation: {discord_parent_path}")

        if not utils.is_discord_running(discord_edition):
            logger.info("")

            # wipe logs, because discord doesn't do that after every updater run
            with open(utils.get_log_file_path(discord_edition), "w") as f:
                f.write("")

            logger.info(f"{discord_edition} is not running. Starting updater.")
            utils.start_discord(discord_edition, discord_parent_path)
            time.sleep(1)

            logger.info(f"Waiting for end of {discord_edition} updating.")
            while utils.is_discord_updating(discord_edition):
                time.sleep(0.5)

        discord_core_folder = utils.get_latest_installed_discord_folder_name(discord_parent_path)
        discord_path = os.path.join(discord_parent_path, discord_core_folder)

        is_last_patch_is_up_to_date = discord_core_folder == config.get_last_installed_discord_version(discord_edition)
        is_bd_injected_already = utils.is_bd_injected(discord_path, config.USE_BD_CI_RELEASES)

        if (
                not is_last_patch_is_up_to_date
                or not is_bd_injected_already
                or bd_has_updates
                or force_update_flag
        ):
            logger.info("")
            logger.info(f"Killing any running {discord_edition} processes...")
            utils.kill_discord(discord_edition)
            time.sleep(2)

            logger.info("")

            if force_update_flag:
                logger.info("Force-set update flags.")
                is_last_patch_is_up_to_date = False
                bd_has_updates = True

            if not is_last_patch_is_up_to_date:
                logger.info(f"{discord_edition} was updated. Verifying injection patch...")
                config.set_discord_version(discord_edition, discord_core_folder)
                config.dump_settings()
                is_bd_injected_already = False

            if not is_bd_injected_already:
                logger.info(f"Verifying BetterDiscord {bd_release_tag} injection patch.")
                utils.inject_patch(discord_path, config.USE_BD_CI_RELEASES)

            if bd_has_updates:
                logger.info(f"BetterDiscord {bd_release_tag} has a new version, updating asar only.")
                utils.update_bd_asar_only(config.USE_BD_CI_RELEASES)
                bd_has_updates = False

            logger.info("")
            logger.info(f"Restarting {discord_edition}...")
            utils.start_discord(discord_edition, discord_parent_path)

            plugins_list = [
                plugins.PluginInfo.from_url("https://raw.githubusercontent.com/riolubruh/YABDP4Nitro/main/YABDP4Nitro.plugin.js")
            ]

            logger.info("")
            for plugin_info in plugins_list:
                logger.info(f"Installing {plugin_info.get_name()} plugin...")
                plugins.download_plugin(plugin_info)
        else:
            logger.info(f"BetterDiscord {bd_release_tag} ({discord_edition}) is up to date and injected. No action needed.")
        logger.info("")

    logger.info("Installation complete. Exiting in 3 seconds...")
    time.sleep(3)
    sys.exit(0)


if __name__ == "__main__":
    main()
