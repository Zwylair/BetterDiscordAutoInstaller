import os
import sys

try:
    import winreg
    import msvcrt
except ImportError:
    input(
        'Your system is not supported yet to using this script\n'
        '\n'
        'Press ENTER to exit.'
    )
    exit(1)


def cls():
    os.system('cls')


key_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
callback = ''

while True:
    cls()

    if callback:
        print(f'{callback}\n')
        callback = ''

    print(
        '[0] -- Exit\n'
        '[1] -- Add to startup\n'
        '[2] -- Remove from startup'
    )

    got_input = msvcrt.getch().decode('utf-8')

    if got_input in ('0', '1', '2'):
        match got_input:
            case '0':
                sys.exit(0)
            case '1' | '2':
                try:
                    # Open the registry key or create it if it doesn't exist
                    try:
                        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
                    except FileNotFoundError:
                        reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)

                    if got_input == '1':
                        value_name = 'BetterDiscordAutoInstaller'
                        value_data = os.path.join(f'"{os.getcwd()}', 'installer.exe"')
                        winreg.SetValueEx(reg_key, value_name, 0, winreg.REG_SZ, value_data)

                    else:
                        winreg.DeleteValue(reg_key, 'BetterDiscordAutoInstaller')
                    winreg.CloseKey(reg_key)

                except Exception as err:
                    callback = f'An error occurred: {err}'
                else:
                    callback = 'Added' if got_input == '1' else 'Removed'
