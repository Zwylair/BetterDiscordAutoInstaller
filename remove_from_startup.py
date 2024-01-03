import os.path

shortcut_location = f'{os.getenv("appdata")}/Microsoft/Windows/Start Menu/Programs/Startup/BetterDiscord AutoInstaller.lnk'

if os.path.exists(shortcut_location):
    os.remove(shortcut_location)
