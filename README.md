# pyFallout3 Launcher

This is a Fallout 3 launcher replacement.

It is intended to be used together with Steam, so that the Steam ingame Overlay is usable and Steam counts ingame Time, while still using Mod Organizer for mod management.

## Installation

* Download the [ZIP file](https://github.com/masterodie/pyfallout3launcher/releases/download/v0.3/pyFallout3Launcher_0.3.zip)
* In your Fallout 3 installation directory (e.g. C:\Program Files\Steam\SteamApps\common\Fallout 3 goty):
* Rename `FalloutLauncher.exe` to `FalloutLauncher_ORG.exe`
* Copy over `FalloutLauncher.exe` from the zip file

## Usage

* Launch the game through Steam
* You can also add Launch parameters through Steam.

        # Path Management
        --fo3-path PATH_TO_EXE
            The path to Fallout3.exe (Default: 'Fallout3.exe')
        --launcher-path PATH_TO_EXE
            The path to FalloutLauncher_ORG.exe (Defalut: 'FalloutLauncher_ORG.exe')
        --fose-path PATH_TO_EXE
            The path to fose_loader.exe (Default 'fose_loader.exe')
        --mo-path PATH_TO_EXE
            the path to ModOrganizer.exe (Default: 'ModOrganizer/ModOrganizer.exe')

        # Launch Applications
        --fo3 - Start Fallout 3
        --launchher - Start the Original Game Launcher
        --fose - Start Fallout Script Extender
        --mo - Start Mod Organizer

        # Mod Organizer Settings
        --use-mo <true/false> - Use ModOrganizer's virtual filesystem
        --profile NAME - The ModOrganizer profile to use

## Requirements for Building
* [Python 2](https://www.python.org)
* [pywin32](http://sourceforge.net/projects/pywin32/)
* [pyinstaller](https://pypi.python.org/pypi/PyInstaller/2.0)

## Building

* Install [Python 2.7 32 Bit](https://www.python.org)
* Install `pywin32` from [sourceforge](http://sourceforge.net/projects/pywin32/
* install pyinstaller with `pip install pyinstaller`
* Build with `pyinstaller falloutlauncher.spec`
* Files will be in `dist`

