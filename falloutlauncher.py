"""
Fallout 3 Launcher Replacement
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
import logging
import os
import subprocess
import sys

import Tkinter as tk
import ttk

try:
    from msvcrt import getch
except:
    logging.error('This program is for Windows only')
    sys.exit(1)

FALLOUT_PATH = os.path.dirname(os.path.realpath(__file__))
FALLOUT = ['Fallout 3', 'Fallout3.exe']
FALLOUT_LAUNCHER = ['Launcher', 'FalloutLauncher_ORG.exe']
FOSE = ['Fallout Script Extender', 'fose_loader.exe']
MOD_ORGANIZER = ['Mod Organizer',
                 os.path.join('ModOrganizer', 'ModOrganizer.exe')]


def str2bool(val):
    return val.lower() in ('yes', 'true', 't', 'y', '1',)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Steam Fallout 3 Launcher replacement"
    )

    parser.register('type', 'bool', str2bool)

    launcher_warning = \
        "(If launching through Mod Organizer this is only for configuration!)"
    prog = parser.add_mutually_exclusive_group()
    prog.add_argument(
        '--launcher',
        action='store_true',
        help='Start Fallout 3 Launcher <{}> {}'.format(FALLOUT_LAUNCHER[1],
                                                       launcher_warning),
    )
    prog.add_argument(
        '--fo3',
        action='store_true',
        help='Start Fallout 3 <{}>'.format(FALLOUT[1]),
    )
    prog.add_argument(
        '--fose',
        action='store_true',
        help='Start Fallout Script Extender <{}>'.format(FOSE[1]),
    )
    prog.add_argument(
        '--mo',
        action='store_true',
        help='Start ModOrganizer <{}>'.format(MOD_ORGANIZER[1])
    )

    modorganizer = parser.add_argument_group(
        "Mod Organizer Specific Options"
    )
    modorganizer.add_argument('--profile', help='The Mod Organizer Profile',
                              default='Default')
    modorganizer.add_argument(
        '--use-mo',
        help='Launch FOSE and Fallout through Mod Organizer',
        type='bool',
        default=True,
    )

    paths = parser.add_argument_group("Application Paths")
    paths.add_argument('--launcher-path',
                       help='Path to original FalloutLauncher.exe',
                       default=FALLOUT_LAUNCHER[1])
    paths.add_argument('--fo3-path',
                       help='Path to Fallout.exe',
                       default=FALLOUT[1])
    paths.add_argument('--fose-path',
                       help='Path to fose_loader.exe',
                       default=FOSE[1])
    paths.add_argument('--mo-path',
                       help='Path to ModOrganizer.exe',
                       default=MOD_ORGANIZER[1])
    paths.add_argument('--fallout-dir',
                       help='Path to Fallout 3 Directory',
                       default=FALLOUT_PATH)

    misc = parser.add_argument_group('Misc')
    misc.add_argument('--loglevel', help='Log level', default="WARNING")

    return parser

parser = parse_arguments()
args = parser.parse_args()

logging.basicConfig(filename='pyFallout3Launcher.log', level=getattr(logging,
                                                                     args.loglevel.upper()))


FALLOUT[1] = args.fo3_path
FALLOUT_LAUNCHER[1] = args.launcher_path
FOSE[1] = args.fose_path
MOD_ORGANIZER[1] = args.mo_path


def mod_organizer(app):
    drive, mo = os.path.splitdrive(MOD_ORGANIZER[1])
    if drive is None:
        mo = os.path.join(FALLOUT_PATH, MOD_ORGANIZER[1])
    drive, application = os.path.splitdrive(app[1])
    if drive is None:
        application = os.path.join(FALLOUT_PATH, app[1])
    retval = application
    if os.path.exists(mo) and (app != MOD_ORGANIZER and
                               app != FALLOUT_LAUNCHER):
            retval = (mo, '-p', args.profile, application)
    loggig.debug(retval)
    return retval


def run_app(app):
    fallout = os.path.join(FALLOUT_PATH, FALLOUT[1])
    if not os.path.exists(fallout):
        message = '''Fallout 3 not found!

Please install this to your Fallout 3 directory!

Installation procedure:
    - Rename FalloutLauncher.exe to FalloutLauncher_ORG.exe
    - Copy over falloutlauncher.exe your Fallout 3 directory
    - Run through steam :)
'''
        logging.error('Fallout 3 Not found. Refer to README.md')

        return 2
    drive, path = os.path.splitdrive(app[1])
    if drive is None:
        path = os.path.join(FALLOUT_PATH, app[1])
    if os.path.exists(path):
        if args.use_mo:
            path = mod_organizer(app)
        logging.info("Running {}".format(app[0]))
        subprocess.Popen(path)
        return 0
    else:
        logging.error("{} executable <{}> does not exist!".format(app[0], path))
        return 1

class GUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, padx=5, pady=4)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.titleLabel = ttk.Label(
            self,
            text='Fallout 3 Launcher',
            font = 'Helvetica 14 bold'
        )
        self.titleLabel.grid(pady=2, sticky=tk.N+tk.E+tk.W)
        self.fo3Button = ttk.Button(
            self,
            text=FALLOUT[0],
            command=self.run_fo3,
            width=25
        )
        self.fo3Button.grid(pady=2, sticky=tk.N+tk.E+tk.W)
        self.launcherButton = ttk.Button(
            self,
            text=FALLOUT_LAUNCHER[0],
            command=self.run_launcher,
            width=25
        )
        self.launcherButton.grid(pady=2, sticky=tk.N+tk.E+tk.W)
        self.foseButton = ttk.Button(
            self,
            text=FOSE[0],
            command=self.run_fose,
            width=25
        )
        self.foseButton.grid(pady=2, sticky=tk.N+tk.E+tk.W)
        self.moButton = ttk.Button(
            self,
            text=MOD_ORGANIZER[0],
            command=self.run_mo,
            width=25
        )
        self.moButton.grid(pady=2, sticky=tk.N+tk.E+tk.W)
        self.quitButton = ttk.Button(
            self,
            text='Quit',
            command=self.quit,
            width=25
        )
        self.quitButton.grid(pady=2, sticky=tk.S+tk.E+tk.W)

    def run_fo3(self):
        run_app(FALLOUT)

    def run_launcher(self):
        run_app(FALLOUT_LAUNCHER)

    def run_fose(self):
        run_app(FOSE)

    def run_mo(self):
        run_app(MOD_ORGANIZER)


def user_input():
    launcher_warning = ""
    if args.use_mo:
        launcher_warning = "(Only for configuration!)"
    print "Fallout 3 Launcher replacement"
    print
    print "<1>\tStart Fallout 3\t\t\t<{}>".format(FALLOUT[1])
    print "<2>\tStart Fallout 3 Launcher\t<{}> {}".format(FALLOUT_LAUNCHER[1],
                                                          launcher_warning)
    print "<3>\tStart Fallout Script Extender\t<{}>".format(FOSE[1])
    print "<4>\tStart Mod Organizer\t\t<{}>".format(MOD_ORGANIZER[1])
    print "<ESC>\tQuit"
    print

    while True:
        choice = getch()
        if choice == "1":
            run_app(FALLOUT)
        elif choice == "2":
            run_app(FALLOUT_LAUNCHER)
        elif choice == "3":
            run_app(FOSE)
        elif choice == "4":
            run_app(MOD_ORGANIZER)
        elif choice == chr(27):
            sys.exit(0)


def main():

    #if args.fo3:
        #run_app(FALLOUT)
    #elif args.launcher:
        #run_app(FALLOUT_LAUNCHER)
    #elif args.fose:
        #run_app(FOSE)
    #elif args.mo:
        #run_app(MOD_ORGANIZER)
    #else:
        #user_input()

    app = GUI()
    app.master.title('Fallout 3 Launcher')
    app.mainloop()


if __name__ == '__main__':
    main()
