<h1 align="center">
    BetterDiscordAutoInstaller
</h1>

<p align="center">
    <img src="https://img.shields.io/badge/python-3.11-green?logo=python&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge">
    <img src="https://img.shields.io/github/languages/code-size/Zwylair/BetterDiscordAutoInstaller?style=for-the-badge">
</p>

## About

`BetterDiscordAutoInstaller` is a script that has the functionality of the official [BetterDiscord installer](https://betterdiscord.app/) of applying this mod on Discord (non canary, etc.). It automatically downloads `betterdiscord.asar` file from the official [BetterDiscord GitHub repo](https://github.com/BetterDiscord/BetterDiscord) and adds into loading modules.

`BetterDiscordAutoInstaller` also allows you to add/remove it from autostart, without having to run it manually every time (only Windows for now) (use `startup_manager`).

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
py installer.py
```

## License

This project is under the [MIT license](./LICENSE).
