#!/usr/bin/env python2.7
"""Celery worker status checker"""

import sys

class NagiosPlugin(object):
    """Nagios Plugin base class"""

    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    def __init__(self, warning, critical, *args, **kwargs):
        self.warning = warning
        self.critical = critical

    def run_check(self):
        raise NotImplementedError

    def ok_state(self, msg):
        print "OK - {}".format(msg)
        sys.exit(self.OK)

    def warning_state(self, msg):
        print "WARNING - {}".format(msg)
        sys.exit(self.WARNING)

    def critical_state(self, msg):
        print "CRITICAL - {}".format(msg)
        sys.exit(self.CRITICAL)

    def unknown_state(self, msg):
        print "UNKNOWN - {}".format(msg)
        sys.exit(self.UNKNOWN)
