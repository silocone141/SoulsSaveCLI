# SoulsSaveCLI


## Introduction

SoulsSaveCLI is a CLI tool designed to manage save files for FromSoftware's souls games on PC (*Dark Souls I-III*, *Sekiro: Shadows Die Twice*, and *Elden Ring*). The tool can be repurposed to work for other games, provided that the game's save files are stored in a similar fashion to FromSoftware's. SoulsSaveCLI was primarily developed with the Linux user in mind, though it is compatible with Windows so long as Python is installed.

SoulsSaveCLI was built using [Click](https://click.palletsprojects.com/en/stable/).


### Prerequisites

Python is required; if you run Linux this will already be installed. If you are on Windows, you will need to install [Python](https://www.python.org/).

This tool has only been tested with Steam, but it should work with other platforms as long as you can access the game's save file.


## Installation


### Using pip

```
pip install soulsave-cli
```

It is recommnded to install this tool in a virtual environment. This way, you can have multiple instances of the tool in different directories, each corresponding to a different game or run. For example, we'll say we would like to set up the tool to use on *Elden Ring*. Suppose we have a directory named `EldenRingRuns/` that we'd like to use as the root directory of our save states, execute:

```
cd path/to/EldenRingRuns

# Create a directory .venv/ and create a virtual environment within
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```

Once done, execute:

```
pip install soulsave-cli
```


### Building locally

Download the lastest tag and move the contents to the directory you'd like to use for the tool. Once done, enter the directory in the terminal and execute:

```
python -m venv .venv
source .venv/bin/activate

pip install --editable .
```

You should then be able to start using the tool.


## Getting Started

If you decided to install `soulsave` in a virtual environment, you will need to activate the virtual environment first with `source .venv/bin/activate`, where `.venv` is the directory of the virtual environment. Once done, you can begin to use the CLI with `soulsave`.

The first thing you should do is run `soulsave init` to set the variables of the configuration file. You will be asked to provide the path to the game's save file directory and the name of the save file itself.


### Where to find the game's save file

<details><summary>Linux</summary>

The save file location will vary from game to game, but a good starting point is to find the directory that hosts Steam's data (for example, `~/.local/share/Steam/`, though this will vary from distribution to distribution).

Once you find Steam's folder, you will need to navigate to `Steam/steamapps/compatdata/`. Within this directory, you will see folders with numerical names. These numbers correspond to the Steam ID of your games. You will need to navigate to the folder named with the corresponding Steam ID of the game you'd like to set up. For this example, we will use `1245620`, *Elden Ring*'s Steam ID.

Below is a table will the *possible* save locations for the various FromSoftware souls games. This could vary by distribution, so treat these paths as a starting point. (Let `$steam` be the path to your Steam directory and `<numeric_steam_id>` is a number generated by Steam.)

| Game | Steam ID | Example Location of Save File | Save File Name |
| ---- | -------- | ----------------------------- | -------------- |
| *Dark Souls Remastered* | 570940 | `$steam/steamapps/compatdata/570940/pfx/drive_c/users/steamuser/My Documents/NBGI/DARK SOULS REMASTERED/<numeric_steam_id>` | `DRAKS0005.sl2` |
| *Dark Souls II: Scholars of the First Sin* | 335300 | | |
| *Dark Souls III* | 374320 | `$steam/steamapps/compatdata/374320/pfx/drive_c/users/steamuser/AppData/Roaming/DarkSoulsIII/<numeric_steam_id>` | `DS30000.sl2` |
| *Sekiro: Shadows Die Twice* | 814380 | `$steam/steamapps/compatdata/814380/pfx/drive_c/users/steamuser/Application Data/Sekiro/<numeric_steam_id>` | `S0000.sl2` |
| *Elden Ring* | 1245620 | `$steam/steamapps/compatdata/1245620/pfx/drive_c/users/steamuser/AppData/Roaming/EldenRing/<numeric_steam_id>` | `ER0000.sl2` |

</details>

<details><summary>Windows</summary>

See [this](https://github.com/Kahmul/SoulsSpeedruns-Save-Organizer?tab=readme-ov-file#savefile-locations) section of this SoulsSpeedrun's Save Organizer README. This tool is a great GUI option for managing saves as well.

</details>


### Populating the configuration file

To populate the configuration file, you can either update `config.yaml` in the installation directory or execute

```
soulsave init
```

to be prompted for the key values of the file. The options of `config.yaml` are:

| Field | Description |
| ----- | ----------- |
| `save_file` | The name of the save file in the game folder |
| `save_location` | The path to the game folder where the save file is stored |
| `save_states_folder` | The path to the location where you'd like to store the save states (this defaults to `SaveStates/` in the project folder, it is recommneded to leave this prompt blank to use the default) |
| `last_loaded` | Leave this blank if editing `config.yaml` directly; this field is not prompted by `soulsave init` |
