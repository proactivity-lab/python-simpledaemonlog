"""logsetup.py: A simple python logging setup for console and local log files."""

__author__ = 'Raido Pahtma'
__license__ = "MIT"

import os
import time
import sys
import logging

DEFAULT_FORMAT_STRING = '%(asctime)s|%(levelname)8s|%(name)10s|%(lineno)3s| %(message)s'


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


def setup_console(level=logging.NOTSET, fs=DEFAULT_FORMAT_STRING):
    console = logging.StreamHandler()
    console.addFilter(PrintfFilter())

    formatter = logging.Formatter(fs)
    console.setFormatter(formatter)
    console.setLevel(level)

    rootlogger = logging.getLogger("")
    rootlogger.setLevel(min(level, rootlogger.getEffectiveLevel()))
    rootlogger.addHandler(console)


def setup_file(application_name, log_folder="log", level=logging.NOTSET, fs=DEFAULT_FORMAT_STRING):
    """
     Directs printf to file with INFO level.
    """
    if not os.path.isdir(log_folder):
        os.makedirs(log_folder)

    utc = time.gmtime()
    ts = time.strftime("%Y%m%d_%H%M%S%Z", utc)

    logfilename = "log_{}_{}.txt".format(application_name, ts)
    logfile = logging.FileHandler(os.path.join(log_folder, logfilename))

    formatter = logging.Formatter(fs)
    logfile.setFormatter(formatter)
    logfile.setLevel(level)

    rootlogger = logging.getLogger("")
    rootlogger.setLevel(min(level, rootlogger.getEffectiveLevel()))
    rootlogger.addHandler(logfile)

    sys.stderr = StdLogger(sys.stderr, logging.error)
    sys.stdout = StdLogger(sys.stdout, logging.info)


if __name__ == "__main__":
    setup_console()
    setup_file("logsetup_test")

    log = logging.getLogger(__name__)

    log.info("A piece of info")
    log.debug("Some debug")
    log.warning("A small warning")
    log.error("A big error")
    try:
        raise TypeError("An ugly TypeError")
    except TypeError:
        log.exception("The description of an exception")

    print("The fine print")