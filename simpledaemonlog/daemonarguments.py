"""daemonarguments.py: Common argparse options for daemons with simpledaemonlog."""

from simpledaemonlog import logsetup

__author__ = 'Raido Pahtma'
__license__ = "MIT"


def arg_str2bool(v):
    """ Use this for boolean options, regular bool is always treated as True. """
    return v.lower() in ("yes", "y", "true", "t", "1")


def add_daemon_arguments(parser):
    parser.add_argument("--daemon", default=False, type=arg_str2bool, help="Daemon mode, no logging to console.")
    parser.add_argument("-d", dest="daemon", action="store_true", help="Daemon mode, no logging to console.")
    parser.add_argument("--logdir", default=None, help="Folder where logfiles should be stored.")
    parser.add_argument("--colorlog", default=False, type=arg_str2bool, help="Color logs for terminal output.")


def setup_daemon(args, name):
    if args.daemon is False:
        logsetup.setup_console(color=args.colorlog)

    if args.logdir is not None:
        logsetup.setup_file(name, logdir=args.logdir)
    elif args.daemon:
        print "WARNING Logging not configured!"
        print args
