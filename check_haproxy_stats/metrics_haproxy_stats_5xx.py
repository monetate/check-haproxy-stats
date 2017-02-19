#!/usr/bin/env python

from __future__ import print_function

import argparse
import socket
import subprocess
import sys

from . import haproxy_util

RETURN_CODES = {"OK": 0, "WARNING": 1, "CRITICAL": 2, "UNKNOWN": 3}


def unknown_exception(f):
    """A decorator to catch all other uncaught exceptions and return unknown code."""
    def f_wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print("Encounter exception {0}".format(repr(e)[:256]))
            return RETURN_CODES["UNKNOWN"]

    return f_wrapper


def _get_parser():
    """Return an argparse parser.

    :return: an argparse.ArgumentParser that would take in appropriate user input
    :rtype: :py:class:`argparse.ArgumentParser`
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--backend", required=True, help="Backend to check 5xx ratio.")
    parser.add_argument("--base-url-path", default="127.0.0.1/haproxy/stats")
    parser.add_argument("--username", required=True, help="Username to login to haproxy stats page.")
    parser.add_argument("--password", required=True, help="Password to login to haproxy stats page.")
    parser.add_argument("--interval", type=int, default=60, help="Time to observe 500 rates (in seconds).")
    parser.add_argument("--gmetric-path", default="/usr/bin/gmetric", help="Path to gmetic bin")
    parser.add_argument("--gmetric-tmax", type=int, default=120, help="gmetric tmax setting")
    parser.add_argument("--gmetric-dmax", type=int, default=150, help="gmetric dmax setting")
    return parser


@unknown_exception
def _report_haproxy_rates(backend, base_url_path, username, password, interval, gmetric_path,
                          gmetric_dmax, gmetric_tmax):
    """Return appropriate exit code and print informational message.

    :return: Exit Code (depending on success)
    :rtype: :py:class:`int`
    """
    hostname = socket.gethostname()
    hrsp_5xx_ratio_interval = haproxy_util.get_hrsp_5xx_ratio(backend, base_url_path, username, password, interval)
    hrsp_5xx_percent_interval = "{0:.2f}".format(hrsp_5xx_ratio_interval * 100)  # convert it to percent
    command = [gmetric_path, "-d", str(gmetric_dmax), "-x", str(gmetric_tmax), "-n",
               "haproxy_{0}_{1}_5xx_percent".format(hostname, backend), "-v", str(hrsp_5xx_percent_interval), "-s",
               "both", "-g", "haproxy", "-t", "float"]
    subprocess.check_call(command)
    return 0


def main():
    """Parser user input and execute the check.

    :return: Exit code (depending on severity).
    :rtype: :py:class:`int`
    """
    parser = _get_parser()
    args = parser.parse_args()
    rc = _report_haproxy_rates(
        backend=args.backend,
        base_url_path=args.base_url_path,
        username=args.username,
        password=args.password,
        interval=args.interval,
        gmetric_path=args.gmetric_path,
        gmetric_dmax=args.gmetric_dmax,
        gmetric_tmax=args.gmetric_tmax)
    return rc


if __name__ == '__main__':
    sys.exit(main())
