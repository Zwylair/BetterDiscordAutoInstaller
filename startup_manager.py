import os
import sys
import winshell

if os.name != 'nt':
    input(
        'Your system is not supported to using this script\n'
        '\n'
        'Press ENTER to exit.'
    )
    sys.exit(0)


link_working_directory = os.path.dirname(__file__)
link_target = sys.executable
link_arguments = os.path.join(link_working_directory, 'main.py')
link_path = os.path.join(
    os.getenv('appdata'),
    r'Microsoft\Windows\Start Menu\Programs\Startup\BetterDiscordAutoInstaller.lnk'
)

if getattr(sys, 'frozen', False):
    link_working_directory = os.path.dirname(sys.executable)
    link_target = os.path.join(link_working_directory, 'main.exe')
    link_arguments = ''

print('BetterDiscordAutoInstaller v1.2.1 (startup_manager)')

while True:
    command = input(
        '[1] -- Add to startup\n'
        '[2] -- Remove from startup\n'
        '\n'
        '> '
    )

    match command:
        case '1':  # no elevation needed
            with winshell.shortcut(link_path) as link:
                link.path = link_target
                link.arguments = link_arguments
                link.working_directory = link_working_directory
                link.description = 'BetterDiscordAutoInstaller v1.2.1'

            print('\n.lnk file of the BetterDiscordAutoInstaller was added to startup.\n')
        case '2':
            os.remove(link_path)
            print('\n.lnk file of the BetterDiscordAutoInstaller was removed from startup.\n')
