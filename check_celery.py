#!/usr/bin/env python2.7
"""Celery worker status checker"""
import argparse
import re
import subprocess
import sys

class NagiosPlugin(object): # pragma: no cover
    OK = 0
    CRITICAL = 2
    UNKNOWN = 3

    def run_check(self):
        raise NotImplementedError

    def ok_state(self, msg):
        print "OK - {}".format(msg)
        sys.exit(self.OK)

    def critical_state(self, msg):
        print "CRITICAL - {}".format(msg)
        sys.exit(self.CRITICAL)

    def unknown_state(self, msg):
        print "UNKNOWN - {}".format(msg)
        sys.exit(self.UNKNOWN)


class CeleryWorkerCheck(NagiosPlugin):
    OK_STATUS_MSG = 'All workers running'
    UNKNOWN_STATUS_MSG = 'Unable to get worker status(es)'

    WORKER_REGEX_TPL = '(\(node {}\))? \(pid \d+\) (is up|is running)'
    CRITICAL_STATUS_MSG_TPL = '{} worker(s) down'

    def __init__(self, workers, service):
        self._workers = workers
        self._service = service
        self._check_cmd = ['service', service, 'status']
        self._status_output = None
        self._critical_workers = []

    def run_check(self):
        try:
            self.status_output = subprocess.check_output(self._check_cmd)
        except subprocess.CalledProcessError:
            self.unknown_state(self.UNKNOWN_STATUS_MSG)

        self._check_status_output()
        self._report_results()

    def _check_status_output(self):
        for worker in self._workers:
            self._check_worker_status(worker)

    def _check_worker_status(self, worker):
        worker_regex = self.WORKER_REGEX_TPL.format(worker)
        worker_status_is_running = re.findall(worker_regex, self.status_output)
        if not worker_status_is_running:
            self._critical_workers.append(worker)

    def _report_results(self):
        if self._critical_workers:
            workers_display = ', '.join(self._critical_workers)
            self.critical_state(self.CRITICAL_STATUS_MSG_TPL.format(workers_display))
        self.ok_state(self.OK_STATUS_MSG)


def main(): # pragma: no cover
    parser = argparse.ArgumentParser(description='Celery worker status checker')
    parser.add_argument('workers', nargs='+', help="Worker node names to check.")
    parser.add_argument('--service', default='celeryd', help="Service script used to manage celery.")
    args = parser.parse_args()

    cwc = CeleryWorkerCheck(args.workers, args.service)
    cwc.run_check()

if __name__ == '__main__': # pragma: no cover
    main()
