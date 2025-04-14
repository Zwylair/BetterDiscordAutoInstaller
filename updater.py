import os
import sys
import shutil
import zipfile
import logging
import requests
import subprocess

import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="(%(asctime)s) %(message)s")


def is_version_greater(first_version: str, second_version: str) -> bool:
    first = first_version.split(".")
    second = second_version.split(".")

    try:
        first = list(map(lambda i: int(i), first))
        second = list(map(lambda i: int(i), second))
    except ValueError:
        print("One of the versions does not match the n.n.n-like version template")
        return False

    if len(first) > len(second):
        second += [0] * (len(first) - len(second))
    elif len(second) > len(first):
        first += [0] * (len(second) - len(first))

    for first_version_number, second_version_number in zip(first, second):
        if first_version_number > second_version_number:
            return True
        elif second_version_number > first_version_number:
            return False
    return False


def get_file_path_without_low_level_folder(file_path: str) -> str:
    """Removes "BetterDiscordAutoInstaller-{tag}/" from "BetterDiscordAutoInstaller-{tag}/main.py"-like path"""
    return "/".join(file_path.split("/")[1:])


def download_file(url: str, save_path: str):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"Failed to download file from {url}. HTTP status code: {response.status_code}")
            sys.exit(1)

        with open(save_path, "wb") as plugin_file:
            plugin_file.write(response.content)
    except Exception as e:
        logger.error(f"An error occurred while downloading file: {e}")
        sys.exit(1)


def clean_folder(path: str, exclude_files: list = ()):
    for file in os.listdir(path):
        if file in exclude_files:
            continue

        try:
            os.remove(file) if os.path.isfile(file) else shutil.rmtree(file)
        except Exception as e:
            logger.error(f"An error occurred while cleaning the {path}: {e}")


def extract_zip(zip_instance: zipfile.ZipFile, target_directory: str):
    for zip_file in zip_instance.filelist:
        if zip_file.is_dir():
            continue

        target_filename = get_file_path_without_low_level_folder(zip_file.filename)
        target_path = os.path.join(target_directory, target_filename)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with zip_instance.open(zip_file, "r") as source_file:
            file_content = source_file.read()

        try:
            with open(target_path, "wb") as target_file:
                target_file.write(file_content)
        except Exception as e:
            logger.error(f"An error occurred while extracting {target_filename}: {e}. Skipping this file...")


def main():
    is_frozen = getattr(sys, "frozen", False)

    if "--run" in sys.argv:
        if is_frozen:
            all_bdai_dirs = [i.lstrip("v") for i in os.listdir() if i.startswith("v") and "main.exe" in os.listdir(i)]
            greatest_version = "0"

            for version in all_bdai_dirs:
                if is_version_greater(version, greatest_version):
                    greatest_version = version

            os.chdir("v" + greatest_version)
            execute_command = ["main.exe"]
        else:
            execute_command = [sys.executable, "main.py"]
        subprocess.run(execute_command)
        sys.exit(1)

    release_url = requests.head(config.BDAI_LATEST_RELEASE_PAGE_URL, allow_redirects=True).url
    latest_version = release_url.split("/")[-1]

    if is_frozen:
        save_path = f"BetterDiscordAutoInstaller-{latest_version}.zip"
        update_package_url = config.BDAI_RELEASE_URL_TEMPLATE.format(tag=latest_version)
        execute_command = ["main.exe"]
        target_directory = os.path.join("./", latest_version)
    else:
        save_path = f"{latest_version}.zip"
        update_package_url = config.BDAI_RAW_RELEASE_URL_TEMPLATE.format(tag=latest_version)
        execute_command = [sys.executable, "main.py"]
        target_directory = "./"

    logger.info("Downloading update package...")
    download_file(update_package_url, save_path)
    update_package = zipfile.ZipFile(save_path)
    logger.info("Downloaded.")

    if os.path.exists(target_directory) and is_frozen:
        logger.info("It seems like the target directory is already exists. Clearing...")
        clean_folder(target_directory)

    logger.info("Unpacking...")
    extract_zip(update_package, target_directory)
    update_package.close()

    logger.info("Cleaning up...")
    try:
        os.remove(save_path)
    except Exception as e:
        logger.info(f"Cannot delete update package ({save_path}): {e}")

    logger.info(f"Update successfully installed. Running main executable with command: {execute_command}\n\n\n")
    os.chdir(target_directory)
    subprocess.run(execute_command)


if __name__ == "__main__":
    main()
