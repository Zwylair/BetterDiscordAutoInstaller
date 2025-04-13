from cx_Freeze import setup, Executable
from config import BDAI_SCRIPT_VERSION

setup(
    name='BetterDiscordAutoInstaller',
    version=BDAI_SCRIPT_VERSION,
    description='',
    executables=[Executable('main.py'), Executable('startup_manager.py')]
)
