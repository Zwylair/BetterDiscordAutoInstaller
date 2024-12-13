import os
import sys
import shutil
import zipfile
import logging
import requests
import subprocess
from funcs import BDAI_LATEST_RELEASE_PAGE_URL, BDAI_RAW_RELEASE_URL_TEMPLATE, BDAI_RELEASE_URL_TEMPLATE

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='(%(asctime)s) %(message)s')

def get_file_path_without_low_level_folder(file_path: str) -> str:
    """Removes "BetterDiscordAutoInstaller-{tag}/" from "BetterDiscordAutoInstaller-{tag}/main.py"-like path"""
    return '/'.join(file_path.split('/')[1:])

def download_file(url: str, save_path: str):
    try:
        logger.info('Downloading file...')

        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as plugin_file:
                plugin_file.write(response.content)
        else:
            logger.error(f"Failed to download file from {url}. HTTP status code: {response.status_code}")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while downloading file: {e}")
        sys.exit(1)

def clean_folder(path: str, exclude_files: list = ()):
    try:
        for file in os.listdir(path):
            if file in exclude_files:
                continue

            if os.path.isfile(file):
                os.remove(file)
            else:
                shutil.rmtree(file)
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)

def extract_zip(zip_instance: zipfile.ZipFile, target_directory: str = '/'):
    try:
        for zip_file in zip_instance.filelist:
            if zip_file.is_dir():
                continue

            filename = zip_file.filename
            target_path = target_directory + get_file_path_without_low_level_folder(filename)

            with zip_instance.open(zip_file, 'r') as source_file:
                file_content = source_file.read()
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            with open(target_path, 'wb') as target_file:
                target_file.write(file_content)
        zip_instance.close()

    except Exception as e:
        logger.error(f'An error occurred while extracting zip: {e}')
        sys.exit(1)

def main():
    is_frozen = getattr(sys, 'frozen', False)
    main_script_execute_command = ['main.exe'] if is_frozen else [sys.executable, 'main.py']
    target_directory = './'

    release_url = requests.head(BDAI_LATEST_RELEASE_PAGE_URL, allow_redirects=True).url
    latest_version = release_url.split('/')[-1]

    # Download another zip if the user is using a non-compiled BDAI
    if is_frozen:
        save_path = f"BetterDiscordAutoInstaller-{latest_version}.zip"
        update_package_url = BDAI_RELEASE_URL_TEMPLATE.format(tag=latest_version)
    else:
        save_path = f'{latest_version}.zip'
        update_package_url = BDAI_RAW_RELEASE_URL_TEMPLATE.format(tag=latest_version)

    download_file(update_package_url, save_path)
    logger.info('Downloaded. Upgrading...')

    update_package = zipfile.ZipFile(save_path)
    clean_folder(target_directory, [save_path, sys.argv[0]])
    extract_zip(update_package, target_directory)
    os.remove(save_path)

    logger.info(f'Upgraded. Running main executable with command: {main_script_execute_command}\n\n\n')
    subprocess.run(main_script_execute_command)

if __name__ == '__main__':
    main()
