"""daemonarguments.py: Common options for daemons with argconfparse and simplelogging."""

import simplelogging.logsetup
from argconfparse.argconfparse import arg_str2bool


__author__ = 'Raido Pahtma'
__license__ = "MIT"


def add_daemon_arguments(parser):
    parser.add_argument("--daemon", default=False, type=arg_str2bool, help="Daemon mode, no logging to console.")
    parser.add_argument("-d", dest="daemon", action="store_true", help="Daemon mode, no logging to console.")
    parser.add_argument("--logdir", default=None, help="Folder where logfiles should be stored.")
    parser.add_argument("--colorlog", default=False, type=arg_str2bool, help="Color logs for terminal output.")


def setup_daemon(args, name):
    if args.daemon is False:
        simplelogging.logsetup.setup_console(color=args.colorlog)

    if args.logdir is not None:
        simplelogging.logsetup.setup_file(name, logdir=args.logdir)
    elif args.daemon:
        print "WARNING Logging not configured!"
        print args
