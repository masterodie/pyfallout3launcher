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
import os
import subprocess
import sys

from msvcrt import getch

FALLOUT_PATH = os.path.dirname(os.path.realpath(__file__))
FALLOUT = ('Fallout 3', 'Fallout3.exe')
FALLOUT_LAUNCHER = ('Launcher', 'FalloutLauncher_ORG.exe')
FOSE = ('Fallout Script Extender', 'fose_loader.exe')
MOD_ORGANIZER = ('Mod Organizer',
                 os.path.join('ModOrganizer', 'ModOrganizer.exe'))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Steam Fallout 3 Launcher replacement"
    )

    prog = parser.add_mutually_exclusive_group()
    prog.add_argument(
        '-launcher',
        action='store_true',
        help='Start Fallout 3 Launcher <{}>'.format(FALLOUT_LAUNCHER[1]),
    )
    prog.add_argument(
        '-fo3',
        action='store_true',
        help='Start Fallout 3 <{}>'.format(FALLOUT[1]),
    )
    prog.add_argument(
        '-fose',
        action='store_true',
        help='Start Fallout Script Extender <{}>'.format(FOSE[1]),
    )
    prog.add_argument(
        '-mo',
        action='store_true',
        help='Start ModOrganizer <{}>'.format(MOD_ORGANIZER[1])
    )
    return parser


parser = parse_arguments()


def run_app(app):
    fallout = os.path.join(FALLOUT_PATH, FALLOUT[1])
    if not os.path.exists(fallout):
        print \
            '''
ERROR: Fallout 3 not found!

Please install this to your Fallout 3 directory!

Installation procedure:
    - Rename FalloutLauncher.exe to FalloutLauncher_ORG.exe
    - Copy over falloutlauncher.exe, python27.dll and MSVCR90.dll to
      your Fallout 3 directory
    - Run through steam :)
'''
        parser.print_help()

        sys.exit(1)
    path = os.path.join(FALLOUT_PATH, app[1])
    if os.path.exists(path):
        print "Running {}".format(app[0])
        subprocess.call(path)
        sys.exit(0)
    else:
        print "{} <{}> does not exist!".format(app[0], path)
        sys.exit(1)


def user_input():
    print "Fallout 3 Launcher replacement"
    print
    print "<1>\tStart Fallout 3\t\t\t<{}>".format(FALLOUT[1])
    print "<2>\tStart Fallout 3 Launcher\t<{}>".format(FALLOUT_LAUNCHER[1])
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

    args = parser.parse_args()

    if args.fo3:
        run_app(FALLOUT)
    elif args.launcher:
        run_app(FALLOUT_LAUNCHER)
    elif args.fose:
        run_app(FOSE)
    elif args.mo:
        run_app(MOD_ORGANIZER)
    else:
        user_input()


if __name__ == '__main__':
    main()
