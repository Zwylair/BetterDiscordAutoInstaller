from cx_Freeze import setup, Executable

# base="Win32GUI" should be used only for Windows GUI app
# base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name='BetterDiscordAutoInstaller',
    version='1.2.4',
    description='',
    executables=[Executable('main.py'), Executable('startup_manager.py')],  # , base=base
)
