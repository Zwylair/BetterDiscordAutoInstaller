
<h1 align="center">
    BetterDiscordAutoInstaller
</h1>

<p align="center">
    <img src="https://img.shields.io/badge/python-3.12-green?logo=python&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge">
    <img src="https://img.shields.io/github/languages/code-size/Zwylair/BetterDiscordAutoInstaller?style=for-the-badge">
</p>

## About

`BetterDiscordAutoInstaller` is a script that do the same work as official [BetterDiscord installer](https://betterdiscord.app/) on applying mod on Discord (PTB, Canary too). It automatically downloads `betterdiscord.asar` file from the official [BetterDiscord GitHub repo](https://github.com/BetterDiscord/BetterDiscord) and makes it load.

Currently, `BetterDiscordAutoInstaller` is supported for **[Windows](https://github.com/Zwylair/BetterDiscordAutoInstaller/tree/master)** and **[macOS](https://github.com/Zwylair/BetterDiscordAutoInstaller/tree/macos)** OSes.

`BetterDiscordAutoInstaller` also allows you to add/remove it from autostart, without having to run it manually every time. For MacOS, the user can also choose to bind script to a keyboard shortcut to manually update.

The script will check if it is up to date. You can disable autoupdate by changing the `disable_bdai_autoupdate` setting to `true` in the `settings.json` file (you will still receive a message that a new version has been released).

## Setup and Dependencies

### Windows

Clone the repository:
```bash
git clone https://github.com/Zwylair/BetterDiscordAutoInstaller
```

Install the dependencies:
```bash
python -m pip install -r requirements.txt
```

Run the script:
```bash
python main.py
```

To add BetterDiscordAutoInstaller to your startup apps:
```bash
python startup_manager.py
```

### MacOS

You need to go to [this](https://github.com/Zwylair/BetterDiscordAutoInstaller/tree/macos?tab=readme-ov-file#setup-and-dependencies) README.md

## Contributing

I will be grateful for any contribution and help given to improve the quality of the project :)

_(especially about adapting the project to other platforms like linux, etc :3)_

### macOS
There is redundant/repetitive code which is seen both in manual-installer-mac.py and auto-installer-mac.py. 

That can be fixed. Just need to make sure to have 2 seperate files to allow for auto, manual install, and auto/manual-mixed functionalities. 

### Fork
Well, just fork it

**But please, don't forget to mention original project in your README**

## License
This project is under the [MIT license](./LICENSE).
