import sys
from cx_Freeze import setup, Executable

# base="Win32GUI" should be used only for Windows GUI app
# base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="BetterDiscordAutoInstaller",
    version="1.1.0",
    description="",
    executables=[Executable("installer.py"), Executable("startup_manager.py")],  # , base=base
)
