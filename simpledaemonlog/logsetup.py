"""logsetup.py: A simple python logging setup for console and local log files."""

import os
import time
import sys
import logging.config
import logging.handlers
import yaml

import logging
log = logging.getLogger(__name__)


__author__ = 'Raido Pahtma'
__license__ = "MIT"

DEFAULT_FORMAT_STRING = '%(asctime)s|%(levelname)8s|%(module)20s|%(lineno)4s| %(message)s'
COLORED_FORMAT_STRING = '%(log_color)s%(asctime)s%(reset)s|%(module)20s|%(lineno)4s| %(log_color)s%(message)s'


class StdLogger(object):
    def __init__(self, out, log):
        self._out = out
        self._log = log
        self.isatty = sys.__stdout__.isatty()

    def _wrt_flt_std_log(self, txt):
        if len(txt) > 0:
            self._log(txt)

    def write(self, txt):
        self._out.write(txt)
        self._wrt_flt_std_log(txt.rstrip())


class PrintfFilter(object):

    def filter(self, record):
        if record.funcName == "_wrt_flt_std_log":
            return 0
        else:
            return True


def _load_settings(path=None):
    if path is not None and os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
        return path
    return None


def setup_console(level=logging.NOTSET, fs=DEFAULT_FORMAT_STRING, settings=None, color=False):
    loaded = _load_settings(settings)

    console = logging.StreamHandler()
    console.addFilter(PrintfFilter())

    if color:
        """ https://pypi.python.org/pypi/colorlog """
        from colorlog import ColoredFormatter
        formatter = ColoredFormatter(
            COLORED_FORMAT_STRING, datefmt=None, reset=True,
            log_colors={
                #'DEBUG':    'cyan',
                'INFO':     'white',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={},
            style='%'
        )
    else:
        formatter = logging.Formatter(fs)

    console.setFormatter(formatter)
    console.setLevel(logging.NOTSET)

    rootlogger = logging.getLogger("")
    rootlogger.setLevel(min(level, rootlogger.getEffectiveLevel()))
    rootlogger.addHandler(console)
    if loaded:
        log.debug("logging config loaded from {:s}".format(loaded))


def setup_file(application_name, logdir="log", level=logging.NOTSET, fs=DEFAULT_FORMAT_STRING, settings=None, backups=8, backupInterval=1, backupIntervalUnit="W6"):
    """
     Directs printf to file with INFO level.
    """
    if not os.path.isdir(logdir):
        os.makedirs(logdir)

    loaded = _load_settings(settings)

    utc = time.gmtime()
    ts = time.strftime("%Y%m%d_%H%M%S%Z", utc)

    logfilename = "log_{}_{}.txt".format(application_name, ts)
    loglatest = "log_{}_latest.txt".format(application_name)
    logfilepath = os.path.join(logdir, logfilename)
    loglinkpath = os.path.join(logdir, loglatest)
    if backups:
        logfile = logging.handlers.TimedRotatingFileHandler(logfilepath, backupCount=backups, when=backupIntervalUnit, interval=backupInterval)
    else:
        # Expect logrotate to pull the file out from underneath us
        logfile = logging.WatchedFileHandler(logfilepath)

    if hasattr(os, "symlink"):
        if os.path.islink(loglinkpath):
            os.unlink(loglinkpath)
        os.symlink(logfilename, loglinkpath)

    formatter = logging.Formatter(fs)
    logfile.setFormatter(formatter)
    logfile.setLevel(logging.NOTSET)

    rootlogger = logging.getLogger("")
    rootlogger.setLevel(min(level, rootlogger.getEffectiveLevel()))
    rootlogger.addHandler(logfile)

    sys.stderr = StdLogger(sys.stderr, logging.error)
    sys.stdout = StdLogger(sys.stdout, logging.info)
    if loaded:
        log.debug("logging config loaded from {:s}".format(loaded))


if __name__ == "__main__":
    setup_console()
    setup_file("logsetup_test")

    log = logging.getLogger(__name__)

    log.debug("Some debug")
    log.info("A piece of info")
    log.warning("A small warning")
    log.error("A big error")
    log.critical("A critical message")

    try:
        raise TypeError("An ugly TypeError")
    except TypeError:
        log.exception("The description of an exception")

    print("The fine print")
