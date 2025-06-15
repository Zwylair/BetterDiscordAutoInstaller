import os
import sys

from win32com.client import Dispatch

import config


def main():
    if os.name != "nt":
        input(
            "Your system is not supported to use this script\n"
            "\n"
            "Press ENTER to exit."
        )
        sys.exit(0)

    print(f"BetterDiscordAutoInstaller v{config.BDAI_SCRIPT_VERSION} (startup_manager)")

    link_working_directory = os.path.dirname(__file__)
    link_target = sys.executable
    link_arguments = os.path.join(link_working_directory, "main.py")
    uv_target = os.path.join(os.path.dirname(sys.executable), "bdai-headless.exe")
    if getattr(sys, "frozen", False):
        link_working_directory = os.path.dirname(sys.executable)
        link_working_directory = os.path.split(link_working_directory)[0]  # a/b/c/ -> a/b/
        link_target = os.path.join(link_working_directory, "updater.exe")
        link_arguments = "--run"
    elif os.path.isfile(uv_target):
        config.load_settings()
        link_working_directory = config.DISCORD_PARENT_PATH
        link_target = uv_target
        link_arguments = ""
    link_path = os.path.join(
        os.getenv("appdata"),
        r"Microsoft\Windows\Start Menu\Programs\Startup\BetterDiscordAutoInstaller.lnk"
    )

    while True:
        command = input(
            "\n"
            "[0] -- Exit\n"
            "[1] -- Add to startup\n"
            "[2] -- Remove from startup\n"
            "\n"
            "> "
        )
        print()

        if command == "0":
            print("Exiting...")
            break
        elif command == "1":
            try:
                shell = Dispatch("WScript.Shell")
                link = shell.CreateShortCut(link_path)
                link.TargetPath = link_target
                link.Arguments = link_arguments
                link.WorkingDirectory = link_working_directory
                link.Description = f"BetterDiscordAutoInstaller v{config.BDAI_SCRIPT_VERSION}"
                link.save()
                print(".lnk file of the BetterDiscordAutoInstaller was added to startup.")

            except PermissionError:
                print("Permission denied. Please run the script with administrator privileges.")
            except Exception as e:
                print(f"An error occurred while adding the shortcut: {e}")
        elif command == "2":
            try:
                if os.path.exists(link_path):
                    os.remove(link_path)
                    print("BetterDiscordAutoInstaller was removed from startup.")
                else:
                    print("The shortcut does not exist in the startup folder.")
            except Exception as e:
                print(f"An error occurred while removing the shortcut: {e}")
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
