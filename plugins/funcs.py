import logging

import requests

from plugins.classes import *

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="(%(asctime)s) %(message)s")


def download_plugin(plugin_info: PluginInfo):
    if plugin_info.is_installed():
        logger.info(f"Plugin {plugin_info.get_name()} already exists.")
        return

    plugin_dir = os.path.dirname(plugin_info.save_path)
    if not os.path.exists(plugin_dir):
        os.makedirs(plugin_dir)

    try:
        logger.info(f"Downloading {plugin_info.get_name()}...")

        response = requests.get(plugin_info.url)
        if response.status_code != 200:
            logger.error(f"Failed to download plugin from {plugin_info.url}: {response.status_code}")
            return

        with open(plugin_info.save_path, "wb") as plugin_file:
            plugin_file.write(response.content)
    except Exception as e:
        logger.error(f"An error occurred while downloading the plugin: {e}")
