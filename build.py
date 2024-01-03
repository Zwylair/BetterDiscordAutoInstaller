import os
import time
import shutil
import subprocess
from datetime import datetime
import psutil


class Executable:
    def __init__(self, filepath: str, allow_console: bool = True, icon_path: str | None = None):
        self.filepath = filepath
        self.allow_console = allow_console
        self.icon_path = icon_path  # allowed: png, ico


PYTHON_INTERPRETER_PATH = f'{os.getenv("localappdata")}/programs/python/python311/python.exe'
REQ_PACKAGES = ['nuitka==1.9.3']
COPY_DIRS = []
COPY_FILES = []
EXECUTABLES = [
    Executable('installer.py', False),
    Executable('starter.py', False),
    Executable('add_to_startup.py', False),
    Executable('remove_from_startup.py', False),
]


def move_dir_with_overwrite(source_dir: str, target_dir: str):
    for file in os.listdir(source_dir):
        shutil.move(os.path.join(source_dir, file), os.path.join(target_dir, file))


# statisfy requirements

os.system(f'{PYTHON_INTERPRETER_PATH} -m pip install -r requirements.txt')
for i in REQ_PACKAGES:
    os.system(f'{PYTHON_INTERPRETER_PATH} -m pip install {i}')

if os.path.exists('dist'):
    shutil.rmtree('dist')
os.mkdir('dist')


# build
for exe in EXECUTABLES:
    print(f'start building {exe.filepath}')

    args = [
        '--force-stderr-spec=err.log',
        '--standalone',
        '--no-pyi-file',
        '--jobs=4',
        f'--windows-icon-from-ico={exe.icon_path}' if exe.icon_path is not None else '',
        '' if exe.allow_console else '--disable-console'
    ]

    subprocess.Popen(f'cmd /c start cmd /c {PYTHON_INTERPRETER_PATH} -m nuitka {" ".join([i for i in args if i])} {exe.filepath}')
    made_time = datetime.now().strftime('%H:%M:%S')
    exe_no_extension, _ = os.path.splitext(exe.filepath)

    # wait for a while to make sure cmd is started
    time.sleep(2)

    for process in psutil.process_iter(['pid', 'name']):
        process_made_time = datetime.fromtimestamp(process.create_time()).strftime('%H:%M:%S')

        if process_made_time == made_time and process.name() == 'cmd.exe':
            while True:
                try:
                    process.status()  # idle request which causes error when closed
                    time.sleep(1)
                except psutil.NoSuchProcess:
                    move_dir_with_overwrite(f'{exe_no_extension}.dist', 'dist')
                    shutil.rmtree(f'{exe_no_extension}.dist')

                    print(f'{exe.filepath} building finished')
                    break
    print()

print('copying additional files')

for i in COPY_DIRS:
    if isinstance(i, str):
        shutil.copytree(i, f'dist/{i}')
    elif isinstance(i, dict):
        shutil.copytree(i['input'], f'dist/{i["output"]}')

for i in COPY_FILES:
    if isinstance(i, str):
        shutil.copytree(i, f'main.dist/{i}')
    elif isinstance(i, dict):
        shutil.copytree(i['input'], f'dist/{i["output"]}')

print('done')
