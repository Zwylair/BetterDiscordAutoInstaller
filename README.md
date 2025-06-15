<h1 align="center">
    BetterDiscordAutoInstaller
</h1>

<p align="center">
    <img src="https://img.shields.io/badge/python-3.13-green?logo=python&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge">
    <img src="https://img.shields.io/github/languages/code-size/Zwylair/BetterDiscordAutoInstaller?style=for-the-badge">
</p>

## About

BetterDiscordAutoInstaller is a script that do the same work as official [BetterDiscord installer](https://betterdiscord.app/) on
applying mod on Discord (PTB, Canary too). It automatically downloads `betterdiscord.asar` file from the
official [BetterDiscord GitHub repo](https://github.com/BetterDiscord/BetterDiscord) and makes it load. If you have more than one discord
(PTB or/and Canary) installed, BDAI will also patch them. But you need to specify paths to them in
`settings.json`.

### Supported OS

Currently, BetterDiscordAutoInstaller is supported for **[Windows](https://github.com/Zwylair/BetterDiscordAutoInstaller/tree/master)** and **[macOS](https://github.com/Zwylair/BetterDiscordAutoInstaller/tree/macos)** OSes.

### BetterDiscord CI

It is also possible to use [BetterDiscord CI Releases](https://github.com/BetterDiscord/BetterDiscord/actions/workflows/ci.yml).
You need to get a [GitHub Access Token](https://github.com/settings/personal-access-tokens/new)
with access to the public repos and change the `use_betterdiscord_ci_releases` option to `true` in
the `settings.json` file. If you have not entered a token before, BDAI will show the prompt for you.

### Autostart

BDAI also allows you to add/remove it from autostart, without having to run it manually  every time.
For macOS, the user can also choose to bind script to a keyboard shortcut to manually update.

### Self update checks

BDAI will check if it is up to date. You can disable autoupdate by changing the `disable_bdai_autoupdate`
setting to `true` in the `settings.json` file (but you will still receive a message that a new version
has been released).

## Setup and Dependencies

### Windows
- Clone the repository: `git clone https://github.com/Zwylair/BetterDiscordAutoInstaller.git`
- Install the dependencies: `python -m pip install -r requirements.txt`
- Run the script: `python main.py`

To add BetterDiscordAutoInstaller to your startup apps: `python startup_manager.py`

#### [UV](https://docs.astral.sh/uv/)
  - Install the tool: `uv tool install git+https://github.com/Zwylair/BetterDiscordAutoInstaller`
  - Run with: `bdai` (or `uvx bdai` if it wasn't added to PATH)
    - It can easily be updated later with: `uv tool upgrade bdai`
  - `[Optional]` Add to your startup with: `bdai --startup-manager` (`uvx bdai --startup-manager` if not in PATH)

### MacOS
You need to go to [this](https://github.com/Zwylair/BetterDiscordAutoInstaller/tree/macos?tab=readme-ov-file#setup-and-dependencies) README.md

## Building

### Windows
- Clone the repository: `git clone https://github.com/Zwylair/BetterDiscordAutoInstaller.git`
- Install the dependencies: `python -m pip install -r requirements.txt`
- Run the build script: `python setup.py build`

## Contributing
I will be grateful for any contribution and help given to improve the quality of the project :)

_(especially about adapting the project to other platforms like linux, etc. :3)_

### macOS
There is redundant/repetitive code which is seen both in manual-installer-mac.py and auto-installer-mac.py. 

That can be fixed. Just need to make sure to have 2 separate files to allow for auto, manual install, and auto/manual-mixed functionalities. 

### Fork
Well, just fork it

**But please, don't forget to mention original project in your README**

## License
This project is under the [MIT license](./LICENSE).
