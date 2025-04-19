import os
import sys
import shutil
import zipfile
import logging
import subprocess

import requests

import config
from utils import backslash_path, is_version_greater, check_for_bdai_updates

logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s %(message)s")
UPDATED_FILENAME = "updated"


def get_log_file_path() -> str:
    return os.path.join(os.path.dirname(get_updater_path()), "updater.log")


def setup_logging():
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        file_handler = logging.FileHandler(filename=get_log_file_path())
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        logger.info(logger.handlers)


def get_path_without_parent_dir(file_path: str) -> str:
    return "/".join(backslash_path(file_path).split("/")[1:])


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


def clean_folder(path: str, exclude_files: tuple = ()):
    for file in os.listdir(path):
        if file in exclude_files:
            continue

        file_path = os.path.abspath(os.path.join(path, file))

        try:
            os.remove(file_path) if os.path.isfile(file_path) else shutil.rmtree(file_path)
        except Exception as e:
            logger.error(f"An error occurred while cleaning the {path}: {e}")


def extract_zip(zip_instance: zipfile.ZipFile, target_directory: str, exclude_files: tuple[str, ...] = ()):
    for zip_file in zip_instance.filelist:
        if zip_file.is_dir():
            continue

        filename = backslash_path(zip_file.filename)
        if filename in exclude_files:
            continue

        target_filename = get_path_without_parent_dir(filename)
        if not target_filename:
            continue

        target_path = os.path.join(target_directory, target_filename)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with zip_instance.open(zip_file, "r") as source_file:
            file_content = source_file.read()

        try:
            with open(target_path, "wb") as target_file:
                target_file.write(file_content)
        except Exception as e:
            logger.error(f"An error occurred while extracting {target_filename}: {e}. Skipping this file...")


def run_bdai():
    logger.info("Running BDAI...")

    if getattr(sys, "frozen", False):
        all_bdai_dirs = [i.lstrip("v") for i in os.listdir() if i.startswith("v") and "main.exe" in os.listdir(i)]
        greatest_version = "0"

        if not all_bdai_dirs:
            logger.info("BDAI installation is not found. Forcing installing update.")
            subprocess.run([get_updater_path(), "--force"])
            sys.exit(0)

        for version in all_bdai_dirs:
            if is_version_greater(version, greatest_version):
                greatest_version = version

        os.chdir("v" + greatest_version)
        execute_command = ["main.exe"]
    else:
        execute_command = [sys.executable, "main.py"]
    subprocess.run(execute_command)


def exception_hook(exc_type, exc_value, exc_traceback):
   logging.error(
       "Uncaught exception",
       exc_info=(exc_type, exc_value, exc_traceback)
   )
   sys.exit(0)


def get_updater_path() -> str:
    return os.path.realpath(sys.argv[0])


def is_this_instance_replica() -> bool:
    return get_updater_path().endswith(".old.exe")


def get_new_instance_filename() -> str:
    return os.path.join(
        os.path.split(get_updater_path())[0],
        "updater.exe" if is_this_instance_replica() else "updater.old.exe"
    )


def main():
    setup_logging()
    sys.excepthook = exception_hook

    logger.debug(f"Running as {os.path.basename(get_updater_path())}")

    is_frozen = getattr(sys, "frozen", False)
    is_updated = os.path.exists(UPDATED_FILENAME)
    force_update_flag = "--force" in sys.argv
    skip_download_flag = "--skip-download" in sys.argv
    run_flag = "--run" in sys.argv

    if is_frozen and is_updated:
        logger.info("Cleaning up after update...")
        os.remove(get_new_instance_filename())  # delete replica file
        os.remove(UPDATED_FILENAME)

        run_bdai()
        sys.exit(0)

    if not force_update_flag:
        if run_flag or not check_for_bdai_updates():
            logger.info("BDAI is up to date.")
            run_bdai()
            sys.exit(0)

    release_url = requests.head(config.BDAI_LATEST_RELEASE_PAGE_URL, allow_redirects=True).url
    latest_version = release_url.split("/")[-1]
    extract_directory = "./"

    if is_frozen:
        if not is_this_instance_replica():
            logger.info("Copy to updater.old.exe and run it to unlock the updater.exe file")
            new_updater_path = get_new_instance_filename()
            shutil.copy(get_updater_path(), new_updater_path)
            subprocess.Popen(
                [new_updater_path] + sys.argv[1:],
                creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
                close_fds=True
            )
            sys.exit(0)

        save_path = f"BetterDiscordAutoInstaller-{latest_version}.zip"
        update_package_url = config.BDAI_RELEASE_URL_TEMPLATE.format(tag=latest_version)
    else:
        save_path = f"{latest_version}.zip"
        update_package_url = config.BDAI_RAW_RELEASE_URL_TEMPLATE.format(tag=latest_version)

    if not skip_download_flag:
        logger.info("Downloading update package...")
        download_file(update_package_url, save_path)
        logger.info("Downloaded.")

    update_package = zipfile.ZipFile(save_path)

    if is_frozen and os.path.exists(extract_directory):
        logger.info("Clearing target directory...")
        clean_folder(extract_directory, exclude_files=("updater.old.exe", "settings.json", save_path, "updater.log"))

    logger.info("Unpacking...")
    extract_zip(update_package, extract_directory)
    update_package.close()

    if not skip_download_flag:
        try:
            os.remove(save_path)
        except Exception as e:
            logger.info(f"Cannot delete update package ({save_path}): {e}")
    open(UPDATED_FILENAME, "w").close()

    logger.info(f"Update successfully installed. Running new updater...")
    subprocess.Popen(
        get_new_instance_filename(),
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
        close_fds=True
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
