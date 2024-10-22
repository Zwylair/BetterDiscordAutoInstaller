
<h1 align="center">
    BetterDiscordAutoInstaller
</h1>

<p align="center">
    <img src="https://img.shields.io/badge/python-3.12-green?logo=python&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge">
    <img src="https://img.shields.io/github/languages/code-size/Zwylair/BetterDiscordAutoInstaller?style=for-the-badge">
</p>

## About

`BetterDiscordAutoInstaller` is a script that works as the official [BetterDiscord installer](https://betterdiscord.app/). This script applies mod on **default** Discord (non canary, etc.). It automatically downloads `betterdiscord.asar` file from the official [BetterDiscord GitHub repo](https://github.com/BetterDiscord/BetterDiscord) and adds into loading modules.

Currently, `BetterDiscordAutoInstaller` is supported for **[Windows](https://github.com/Zwylair/BetterDiscordAutoInstaller/tree/master)** and **[macOS](https://github.com/Zwylair/BetterDiscordAutoInstaller/tree/macos)** platforms.

For MacOS users, `BetterDiscordAutoInstaller` allows you to bind script to a keyboard shortcut to manually update.

## Setup and Dependencies

This repository contains two Python scripts for automatically installing BetterDiscord on macOS. The scripts provide two different installation methods: one for manual installation with a keyboard shortcut and another for automatic installation on startup.

#### Features
- **Manual Installation with Keyboard Shortcut:** Provides a step-by-step process to manually install BetterDiscord using a keyboard shortcut on macOS.
- **Automatic Installation on Startup:** Automatically installs BetterDiscord when your Mac starts up and detects a Discord update.

#### Installation

Clone the repository and change directory:
```bash
git clone https://github.com/Zwylair/BetterDiscordAutoInstaller
cd BetterDiscordAutoInstaller
```

Create virtual enviornment & activate it:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

#### Usage
##### Manual Installation with Keyboard Shortcut (recommended)
You can just run this script and it would work. However, that's not ideal. We want to be able to run it with just a keyboard shortcut. In order to do that on mac, do the following:

1. Open the `Automator` Application
2. Select `Quick Action` and click "Choose"
3. At the top, change it from 
   1. > Workflow recieves current ***Automatic (text)*** in any application
4. to 
   1. > Workflow recieves current ***no input*** in any application
5. In the search bar on the left, search `Run Shell Script` and double click
6. Use shell script of choice. Example here will be for `/bin/bash`. Type the following:
 ```bash
cd Projects/BetterDiscordAutoInstaller
source venv/bin/activate
pip install -r requirements.txt
python3 macos/manual-installer-mac.py
```
> Reminder: You can update the manual-installer-mac.py code to give you more or less notifications. Feel free to update the local code according to your preferences.
7. Update the directory and virtual enviornment name to whatever you used. This example cloned the repo to the "Projects" directory and named the virtual env "venv".
8. Make sure it's saved and name it something memorable (ex. "Run BetterDiscord Script"). 
9. Run manually to make sure it's working without errors. 
10. Go to `Settings`
11.  Search and click on `Keyboard Shortcuts`
12.  On the left pane, click `Services`
13.  Open the right pane, open the `General` dropdown. You should see the `.workflow` file you created in Automator.
14.  Click `none` and type in whatever keyboard shortcut you want to use. Make sure it doesn't conflict with something else (ex. `cmd + shift + 0`)
15.  Click `done`, click out, and test! 

You're all set! 

##### Automatic Installation on Startup
We'd recommend using the manual installation as it's less resource-intensive. However, if you can't be bothered, this is the script for you!

This script is more resource-intensive as it will continously wait until it Discord updates. Once Discord starts updating, it waits for it to finish, and then patches in BetterDiscord and waits for another update. 

For this script to work, you need to make it run everytime at startup. Here's how to do that. 

1. Open the `Automator` Application
2. Select `Quick Action` and click `Choose`
3. At the top, change it from 
   1. > Workflow recieves current ***Automatic (text)*** in any application
4.  to
      1. > Workflow recieves current ***no input*** in any application
5. In the search bar on the left, search `Run Shell Script` and double click
6. Use shell script of choice. Example here will be for `/bin/bash`. Type the following:
 ```bash
cd Projects/BetterDiscordAutoInstaller
source venv/bin/activate
pip install -r requirements.txt
python3 macos/auto-installer-mac.py
```
> Reminder: You can update the auto-installer-mac.py code to give you more or less notifications. Feel free to update the local code according to your preferences.
7. Update the directory and virtual enviornment name to whatever you used. This example cloned the repo to the "Projects" directory and named the virtual env "venv".
8. Make sure it's saved and name it something memorable (ex. "BetterDiscord AutoInstaller"). 
9. Run manually to make sure it's working without errors. 
10. Go to `Settings`

> Note: this part is different for those who already did the manual installation
11. Search and click on `Open at Login`
12. Click the `+` button and navigate to `~/Library/Services` (you can press ctrl + shift + g and paste for easier naviation)
13. You should see the `.workflow` file you created in Automator. 
14. Select it and hit `done`! 

You're all set! 

### How Each Script Works

#### `manual-installer-mac.py`
The manual-installer-mac.py script allows you to manually install BetterDiscord with a keyboard shortcut. Here’s how it works:


1. **Check for Discord Updates:** Checks if Discord is in the process of updating by monitoring the presence of a "ShipIt" process. It also checks if the update folder is still present, indicating that the update process is not yet complete.

2. **Automatic Patching:** After confirming that the update is complete, the script automatically downloads the latest BetterDiscord .asar file, patches Discord’s index.js file, and replaces existing BetterDiscord.asar file with the latest one.

3. **Manual Execution:** You run this script manually, which gives you control over when and how BetterDiscord is installed. Trigger the installation process yourself, ideally after ensuring that Discord has finished updating.

#### `auto-installer-mac.py`

The auto-installer-mac.py script automates the installation of BetterDiscord whenever Discord updates. Here’s how it works:


1. **Monitoring for Updates:** The script continuously monitors the system to detect when Discord begins an update. It checks for the presence of the "ShipIt" process, which is used by Discord during updates.

2. **Wait for Update Completion:** Once an update is detected, the script waits for the update to finish. It periodically checks to ensure that both the "ShipIt" process has ended and that the update directory has been emptied.

3. **Automatic Patching:** After confirming that the update is complete, the script automatically downloads the latest BetterDiscord .asar file, patches Discord’s index.js file, and replaces existing BetterDiscord.asar file with the latest one.

4. **Continuous Monitoring:** This script runs in the background, continually checking for updates to Discord. It is designed to be run at startup, ensuring BetterDiscord is always reinstalled automatically after any Discord update. 

## Contributing

I will be grateful for any contribution and help given to improve the quality of the project :)

_(especially about adapting the project to other platforms like linux, etc :3)_

### macOS
There is redundant/repetitive code which is seen both in manual-installer-mac.py and auto-installer-mac.py. 

That can be fixed. Just need to make sure to have 2 separate files to allow for auto, manual install, and auto/manual-mixed functionalities. 

### Fork
Well, just fork it

**But please, don't forget to mention original project in your README**

## Special thanks

**[Ajit Mehrotra](https://github.com/Ajit-Mehrotra)** for adding masOS support

## License
This project is under the [MIT license](./LICENSE).
