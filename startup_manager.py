import os
import sys
import winshell
from funcs import BDAI_SCRIPT_VERSION

# Ensure the script is running on Windows
if os.name != 'nt':
    input(
        'Your system is not supported to using this script\n'
        '\n'
        'Press ENTER to exit.'
    )
    sys.exit(0)

# Paths and settings
link_working_directory = os.path.dirname(__file__)
link_target = sys.executable
link_arguments = os.path.join(link_working_directory, 'main.py')
link_path = os.path.join(
    os.getenv('appdata'),
    r'Microsoft\Windows\Start Menu\Programs\Startup\BetterDiscordAutoInstaller.lnk'
)

# Handle frozen state (when the script is packaged as an executable)
if getattr(sys, 'frozen', False):
    link_working_directory = os.path.dirname(sys.executable)
    link_target = os.path.join(link_working_directory, 'main.exe')
    link_arguments = ''

print(f'BetterDiscordAutoInstaller v{BDAI_SCRIPT_VERSION} (startup_manager)')

# Loop for user interaction
while True:
    command = input(
        '[1] -- Add to startup\n'
        '[2] -- Remove from startup\n'
        '[0] -- Exit\n'
        '\n'
        '> '
    )

    if command == '1':  # Add to startup
        try:
            # Create a shortcut in the startup folder
            with winshell.shortcut(link_path) as link:
                link.path = link_target
                link.arguments = link_arguments
                link.working_directory = link_working_directory
                link.description = f'BetterDiscordAutoInstaller v{BDAI_SCRIPT_VERSION}'
            print('\n.lnk file of the BetterDiscordAutoInstaller was added to startup.\n')

        except PermissionError:
            print("\nPermission denied: Please run the script with administrator privileges.\n")
        except Exception as e:
            print(f"\nAn error occurred while adding the shortcut: {e}\n")

    elif command == '2':  # Remove from startup
        try:
            # Remove the shortcut if it exists
            if os.path.exists(link_path):
                os.remove(link_path)
                print('\n.lnk file of the BetterDiscordAutoInstaller was removed from startup.\n')
            else:
                print("\nThe shortcut does not exist in the startup folder.\n")
        except Exception as e:
            print(f"\nAn error occurred while removing the shortcut: {e}\n")

    elif command == '0':  # Exit the script
        print("\nExiting...")
        break

    else:
        print("\nInvalid option. Please choose [1], [2], or [0] to exit.\n")
