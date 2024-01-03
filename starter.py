import sys
import subprocess

arguments = sys.argv[1:]
valid_arguments = ['--silent', '--do-not-start-discord']
start_with_arguments = [i for i in arguments if i in valid_arguments]

if '--silent' in arguments:
    subprocess.run(['installer.exe'] + start_with_arguments, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
else:
    subprocess.run(['installer.exe'] + start_with_arguments)
