import os.path
from win32com.client import Dispatch

target_path = os.path.join(os.getcwd(), 'starter.exe')
shortcut_location = f'{os.getenv("appdata")}/Microsoft/Windows/Start Menu/Programs/Startup/BetterDiscord AutoInstaller.lnk'

if os.path.exists(shortcut_location):
    os.remove(shortcut_location)

shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(shortcut_location)
shortcut.TargetPath = target_path
shortcut.Arguments = '--silent'
shortcut.WorkingDirectory = os.getcwd()
shortcut.save()
