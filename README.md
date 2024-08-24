<h1 align="center">
    BetterDiscordAutoInstaller
</h1>

<p align="center">
    <img src="https://img.shields.io/badge/python-3.12-green?logo=python&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge">
    <img src="https://img.shields.io/github/languages/code-size/Zwylair/BetterDiscordAutoInstaller?style=for-the-badge">
</p>

## About

`BetterDiscordAutoInstaller` is a **Windows-only** script that works as the official [BetterDiscord installer](https://betterdiscord.app/). This script applies mod on **default** Discord (non canary, etc.). It automatically downloads `betterdiscord.asar` file from the official [BetterDiscord GitHub repo](https://github.com/BetterDiscord/BetterDiscord) and adds into loading modules.

`BetterDiscordAutoInstaller` also allows you to add/remove it from autostart, without having to run it manually every time (use `startup_manager`).

## Setup and Dependencies

### Windows

Clone the repository:
```bash
git clone https://github.com/Zwylair/BetterDiscordAutoInstaller
```

Install the dependencies:
```bash
py -m pip install -r requirements.txt
```

Run the script:
```bash
py main.py
```

## Contribution

I will be grateful for any contribution and help given to improve the quality of the project :)

_(especially about adapting the project to other platforms like linux, macos :3)_

## Fork

Well, just fork it

**But please, don't forget to mention original project in your README**

## License

This project is under the [MIT license](./LICENSE).
