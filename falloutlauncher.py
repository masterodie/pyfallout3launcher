"""
pyFallout3 Launcher
Copyright 2015 Patrick Neff

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import argparse
import ConfigParser
import logging
import os
import subprocess
import sys

import Tkinter as tk
import ttk
import tkMessageBox

try:
    from msvcrt import getch
except:
    logging.error('This program is for Windows only')
    sys.exit(1)

FALLOUT_PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = 'pyFallout3Launcher.conf'


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def parse_configfile():
    config = ConfigParser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        config.add_section('Defaults')
        config.set('Defaults', 'fo3_path', 'Fallout3.exe')
        config.set('Defaults', 'launcher_path', 'FalloutLauncher_ORG.exe')
        config.set('Defaults', 'fose_path', 'fose_loader.exe')
        config.set('Defaults', 'mo_path',
                   os.path.join('ModOrganizer', 'ModOrganizer.exe'))
        config.set('Defaults', 'use_mo', 'yes')
        config.set('Defaults', 'gui', 'yes')
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
    config.read(CONFIG_FILE)
    return config


def str2bool(val):
    return val.lower() in ('yes', 'true', 't', 'y', '1',)


def parse_arguments():
    config = parse_configfile()
    defaults = dict(config.items("Defaults"))
    parser = argparse.ArgumentParser(
        description="Steam Fallout 3 Launcher replacement"
    )

    parser.register('type', 'bool', str2bool)

    launcher_warning = \
        "(If launching through Mod Organizer this is only for configuration!)"
    apps = parser.add_argument_group('Launch Applications')
    app = apps.add_mutually_exclusive_group()
    app.add_argument(
        '--launcher',
        action='store_true',
        help='Start Fallout 3 Launcher <{}> {}'.format(
            config.get('Defaults', 'fo3_path'),
            launcher_warning
        ),
    )
    app.add_argument(
        '--fo3',
        action='store_true',
        help='Start Fallout 3 <{}>'.format(
            config.get('Defaults', 'launcher_path')
        ),
    )
    app.add_argument(
        '--fose',
        action='store_true',
        help='Start Fallout Script Extender'.format(
            config.get('Defaults', 'fose_path')
        ),
    )
    app.add_argument(
        '--mo',
        action='store_true',
        help='Start ModOrganizer <{}>'.format(config.get('Defaults', 'mo_path'))
    )

    parser.set_defaults(**defaults)

    modorganizer = parser.add_argument_group(
        "Mod Organizer Specific Options"
    )
    modorganizer.add_argument('--profile', help='The Mod Organizer Profile',
                              default='Default')
    modorganizer.add_argument(
        '--use-mo',
        help='Launch FOSE and Fallout through Mod Organizer',
        type='bool',
        default=config.getboolean('Defaults', 'use_mo'),
    )

    paths = parser.add_argument_group("Application Paths")
    paths.add_argument('--launcher-path',
                       help='Path to original FalloutLauncher.exe',
                       default=config.get('Defaults', 'launcher_path'))
    paths.add_argument('--fo3-path',
                       help='Path to Fallout.exe',
                       default=config.get('Defaults', 'fo3_path'))
    paths.add_argument('--fose-path',
                       help='Path to fose_loader.exe',
                       default=config.get('Defaults', 'fose_path'))
    paths.add_argument('--mo-path',
                       help='Path to ModOrganizer.exe',
                       default=config.get('Defaults', 'mo_path'))
    paths.add_argument('--fallout-dir',
                       help='Path to Fallout 3 Directory',
                       default=FALLOUT_PATH)

    misc = parser.add_argument_group('Misc')
    misc.add_argument('--loglevel', help='Log level', default="WARNING")
    misc.add_argument('--gui', dest='gui', action='store_true')
    misc.add_argument('--no-gui', dest='gui', action='store_false')
    misc.set_defaults(gui=config.getboolean('Defaults', 'gui'))

    args = parser.parse_args()
    return args

args = parse_arguments()

logging.basicConfig(filename='pyFallout3Launcher.log',
                    level=getattr(logging, args.loglevel))


def mod_organizer(app):
    mo = args.mo_path
    drive, mo = os.path.splitdrive(mo)
    if drive is None:
        mo = os.path.join(FALLOUT_PATH, mo)
    drive, app = os.path.splitdrive(app)
    if drive is None:
        app = os.path.join(FALLOUT_PATH, app)
    retval = app
    if os.path.exists(mo) and (app != args.mo_path and
                               app != args.launcher_path):
            retval = (mo, '-p', args.profile, app)
    logging.debug(retval)
    return retval


def run_game(app):
    fallout = os.path.join(FALLOUT_PATH, args.fo3_path)
    if not os.path.exists(fallout):
        logging.error('{} Not found. Refer to README.md'.format(args.fo3_path))
        return 2

    drive, path = os.path.splitdrive(app)
    if drive is None:
        path = os.path.join(FALLOUT_PATH, app)

    if os.path.exists(path):
        if args.use_mo:
            app = mod_organizer(app)
        logging.info("Running {}".format(app))
        subprocess.Popen(app)
        return 0
    else:
        logging.error("{} does not exist!".format(app))
        return 1


class GUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, padx=5, pady=4)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.logo = tk.PhotoImage(file=resource_path(
            os.path.join('assets', 'img',
                         'pyFallout3Launcher_Logo.gif')
        ))
        self.titleLabel = ttk.Label(
            self,
            # text='pyFallout3 Launcher',
            image=self.logo,
            font='Helvetica 14 bold',
            justify=tk.CENTER
        )
        self.titleLabel.image = self.logo
        self.titleLabel.grid(columnspan=2, pady=2, sticky=tk.N+tk.E+tk.W)

        self.fo3Button = ttk.Button(
            self,
            text='Fallout 3',
            command=self.run_fo3,
            width=25
        )
        self.fo3Button.grid(columnspan=2, pady=2, sticky=tk.N+tk.E+tk.W)

        self.launcherButton = ttk.Button(
            self,
            text='Fallout 3 Launcher',
            command=self.run_launcher,
            width=25
        )
        self.launcherButton.grid(columnspan=2, pady=2, sticky=tk.N+tk.E+tk.W)

        self.foseButton = ttk.Button(
            self,
            text='Fallout Script Extender',
            command=self.run_fose,
            width=25
        )
        self.foseButton.grid(columnspan=2, pady=2, sticky=tk.N+tk.E+tk.W)

        self.moButton = ttk.Button(
            self,
            text='Mod Organizer',
            command=self.run_mo,
            width=25
        )
        self.moButton.grid(columnspan=2, pady=2, sticky=tk.N+tk.E+tk.W)

        self.optionsButton = ttk.Button(
            self,
            text='Options',
            command=self.show_options,
            width=15
        )
        self.optionsButton.grid(row=99, column=0, columnspan=1, padx=2, pady=2, sticky=tk.S+tk.E+tk.W)

        self.quitButton = ttk.Button(
            self,
            text='Quit',
            command=self.quit,
            width=10
        )
        self.quitButton.grid(row=99, column=1, columnspan=1, padx=2, pady=2, sticky=tk.S+tk.E+tk.W)

    def run_fo3(self):
        self.run_game(args.fo3_path)
        self.quit()

    def run_launcher(self):
        self.run_game(args.launcher_path)
        if not args.use_mo:
            self.quit()

    def run_fose(self):
        self.run_game(args.fose_path)
        self.quit()

    def run_mo(self):
        self.run_game(args.mo_path)
        self.quit()

    def run_game(self, game):
        retval = run_game(game)
        if retval == 0:
            logging.debug('Execution of {} successful')
        elif retval == 1:
            title = 'Application missing'
            message = 'The application is missing! ({0})'.format(game)
            tkMessageBox.showerror(title, message)
        elif retval == 2:
            title = 'Install Error'
            message = 'The game application is missing! ({0})\n' \
                'Please install this to your Game directory.'.format(
                    args.fo3_path
                )
            tkMessageBox.showerror(title, message)
            self.quit()
            sys.exit(retval)
        else:
            pass

    def show_options(self):
        tkMessageBox.showinfo('Not Implemented', 'Not implemented yet!')


def user_input():
    launcher_warning = ""
    if args.use_mo:
        launcher_warning = "(Only for configuration!)"
    print "pyFallout3 Launcher"
    print
    print "<1>\tStart Fallout 3\t\t\t<{}>".format(args.fo3_path)
    print "<2>\tStart Fallout 3 Launcher\t<{}> {}".format(args.launcher_path,
                                                          launcher_warning)
    print "<3>\tStart Fallout Script Extender\t<{}>".format(args.fose_path)
    print "<4>\tStart Mod Organizer\t\t<{}>".format(args.mo_path)
    print "<ESC>\tQuit"
    print

    while True:
        choice = getch()
        if choice == "1":
            retval = run_game(args.fo3_path)
            sys.exit(retval)
        elif choice == "2":
            retval = run_game(args.launcher_path)
            if not args.use_mo:
                sys.exit(retval)
        elif choice == "3":
            retval = run_game(args.fose_path)
            sys.exit(retval)
        elif choice == "4":
            retval = run_game(args.mo_path)
            sys.exit(retval)
        elif choice == chr(27):
            sys.exit(0)


def main():

    if args.fo3:
        run_game(args.fo3_path)
    elif args.launcher:
        run_game(args.launcher_path)
    elif args.fose:
        run_game(args.fose_path)
    elif args.mo:
        run_game(args.mo_path)
    else:
        if args.gui is False:
            user_input()
        else:
            app = GUI()
            app.master.title('pyFallout3 Lauchner')
            app.mainloop()


if __name__ == '__main__':
    main()
