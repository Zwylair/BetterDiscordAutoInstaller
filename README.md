<h1 align="center" style="font-size: 48px;">
    BetterDiscordAutoInstaller
</h1>

<p align="center">
    <img src="https://img.shields.io/badge/python-3.11-green?logo=python&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge">
    <img src="https://img.shields.io/github/languages/code-size/Zwylair/BetterDiscordAutoInstaller?style=for-the-badge">
</p>

You can't imagine how much of a nuisance it is for me to have to reinstall BetterDiscord **MANUALLY** every time after Discord automatically updates. After searching up the internet, I realised that I wasn't the only one with this problem and I set out to solve it.

**BetterDiscordAutoInstaller** is a program that automatically downloads and patches Discord to the latest version of BetterDiscord when you start Windows OS (only Windows for now).

The program can be removed and added to autorun by the corresponding `remove_from_startup.py` and `add_to_startup.py` scripts, which **no longer requires** your MANUAL downloading and installing 130mb *(!)* official BetterDiscord stuff **EVERY DISCORD UPDATE**.

## Setup and Dependencies

Clone the repository:
```bash
git clone https://github.com/Zwylair/BetterDiscordAutoInstaller
```

Install the dependencies:
```bash
python3 -m pip install -r requirements.txt
```

Run the program:
```bash
python3 main.py
```

## License

This project is under the [MIT license](./LICENSE).
