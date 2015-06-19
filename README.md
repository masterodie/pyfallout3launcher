# Fallout 3 Launcher replacement

## Installation

* Download the [ZIP file](https://github.com/masterodie/pyfallout3launcher/releases/download/v0.1/pyFallout3Launcher_0.1.zip)
* In your Fallout 3 installation directory (e.g. c:\Program Files\Steam\SteamApps\common\Fallout 3 goty):
* Rename `FalloutLauncher.exe` to `FalloutLauncher_ORG.exe`
* Copy over `falloutlauncher.exe`, `python27.dll` and `MSVCRT90.dll` over to your Fallout 3 directory.
* Launch the game through Steam

## Requirements for Building
* [Python 2](https://www.python.org)
* [pywin32](http://sourceforge.net/projects/pywin32/)
* [pyinstaller](https://pypi.python.org/pypi/PyInstaller/2.0)

## Building

* Install `pywin32` from sourceforge
* install pyinstaller with `pip install pyinstaller`
* Build with

        pyinstaller ./falloutlauncher.py

* Files will be in ./dist/falloutlauncher

