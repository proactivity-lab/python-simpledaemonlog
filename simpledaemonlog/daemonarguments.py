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
    parser.add_argument("--rotate_count", default=0, type=int, help="Enable log rotation, keep so many old log files. If 0, log rotation is disabled.")
    parser.add_argument("--rotate_unit", default="W6", type=str, help="When log rotation is enabled, select this time unit ('S':secs, 'M':mins, 'H':hours, 'D':days, 'W0'-'W6':weekday, 'midnight')")
    parser.add_argument("--rotate_interval", default="1", type=int, help="When log rotation is enabled, allow this many time units to elapse before doing the rotation (not used when weekday rotation is selected)")


def setup_daemon(args, name):
    if args.daemon is False:
        logsetup.setup_console(color=args.colorlog)

    if args.logdir is not None:
        logsetup.setup_file(name, logdir=args.logdir, backups=args.rotate_count, backupInterval=args.rotate_interval, backupIntervalUnit=args.rotate_unit)
    elif args.daemon:
        print "WARNING Logging not configured!"
        print args
