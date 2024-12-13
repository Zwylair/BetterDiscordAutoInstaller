from cx_Freeze import setup, Executable
from funcs import BDAI_SCRIPT_VERSION

# base="Win32GUI" should be used only for Windows GUI app
# base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name='BetterDiscordAutoInstaller',
    version=BDAI_SCRIPT_VERSION,
    description='',
    executables=[Executable('main.py'), Executable('startup_manager.py')],  # , base=base
)
