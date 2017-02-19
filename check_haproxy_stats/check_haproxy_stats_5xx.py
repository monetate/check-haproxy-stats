#!/usr/bin/env python

from __future__ import print_function

import argparse
import sys

from . import haproxy_util

RETURN_CODES = {"OK": 0, "WARNING": 1, "CRITICAL": 2, "UNKNOWN": 3}


def unknown_exception(f):
    """A decorator to catch all other uncaught exceptions and return unknown code."""
    def f_wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return _handle_unknown(str(e)[:256])

    return f_wrapper


def _get_parser():
    """Return an argparse parser.

    :return: an argparse.ArgumentParser that would take in appropriate user input
    :rtype: :py:class:`argparse.ArgumentParser`
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--backend", required=True, help="Backend to check 5xx ratio.")
    parser.add_argument(
        "--warning-ratio", type=float, default=0.01, help="500x ratio above which we should throw warning.")
    parser.add_argument(
        "--critical-ratio", type=float, default=0.02, help="500x ratio above which we should throw critical.")
    parser.add_argument("--base-url-path", default="127.0.0.1/haproxy/stats")
    parser.add_argument("--username", required=True, help="Username to login to haproxy stats page.")
    parser.add_argument("--password", required=True, help="Password to login to haproxy stats page.")
    parser.add_argument("--interval", type=int, default=60, help="Time to observe 500 rates (in seconds).")
    return parser


def _get_message(status, backend, hrsp_5xx_ratio, warning_ratio, critical_ratio, interval):
    """Return a message conveying the check results.

    :return: Informational message about the check
    :rtype: :py:class:`str`
    """
    return ("""{backend} traffic has HTTP 5xx ratio of {hrsp_5xx_ratio:.4f} in the past {interval} seconds."""
            """Thresholds: warning: {warning_ratio}, critical: {critical_ratio}""").format(
        backend=backend,
        hrsp_5xx_ratio=hrsp_5xx_ratio,
        interval=interval,
        warning_ratio=warning_ratio,
        critical_ratio=critical_ratio, )


def _handle_critical(backend, hrsp_5xx_ratio, warning_ratio, critical_ratio, interval):
    """Print informational message regarding the check and return CRITICAL exit code.

    :return: Critical Exit Code
    :rtype: :py:class:`int`
    """
    print(_get_message("CRITICAL", backend, hrsp_5xx_ratio, warning_ratio, critical_ratio, interval))
    return RETURN_CODES["CRITICAL"]


def _handle_ok(backend, hrsp_5xx_ratio, warning_ratio, critical_ratio, interval):
    """Print informational message regarding the check and return OK exit code.

    :return: OK Exit Code
    :rtype: :py:class:`int`
    """
    print(_get_message("OK", backend, hrsp_5xx_ratio, warning_ratio, critical_ratio, interval))
    return RETURN_CODES["OK"]


def _handle_warning(backend, hrsp_5xx_ratio, warning_ratio, critical_ratio, interval):
    """Print informational message regarding the check and return WARNING exit code.

    :return: Warning Exit Code
    :rtype: :py:class:`int`
    """
    print(_get_message("WARNING", backend, hrsp_5xx_ratio, warning_ratio, critical_ratio, interval))
    return RETURN_CODES["WARNING"]


def _handle_unknown(exception_message):
    """Print informational message regarding the check and return UNKNOWN exit code.

    :return: Unknown Exit Code
    :rtype: :py:class:`int`
    """
    m = "UNKNOWN: Got the following unhandled exception {0}".format(exception_message)
    print(m)
    return RETURN_CODES["UNKNOWN"]


@unknown_exception
def _check_haproxy_rates(backend, warning_ratio, critical_ratio, base_url_path, username, password, interval):
    """Return appropriate exit code and print informational message.

    :return: Exit Code (depending on severity)
    :rtype: :py:class:`int`
    """
    hrsp_5xx_ratio_interval = haproxy_util.get_hrsp_5xx_ratio(backend, base_url_path, username, password, interval)

    if hrsp_5xx_ratio_interval > critical_ratio:
        handler = _handle_critical
    elif hrsp_5xx_ratio_interval > warning_ratio:
        handler = _handle_warning
    else:
        handler = _handle_ok

    return handler(backend, hrsp_5xx_ratio_interval, warning_ratio, critical_ratio, interval)


def main():
    """Parser user input and execute the check.

    :return: Exit code (depending on severity).
    :rtype: :py:class:`int`
    """
    parser = _get_parser()
    args = parser.parse_args()
    rc = _check_haproxy_rates(backend=args.backend,
                              warning_ratio=args.warning_ratio,
                              critical_ratio=args.critical_ratio,
                              base_url_path=args.base_url_path,
                              username=args.username,
                              password=args.password,
                              interval=args.interval)
    return rc


if __name__ == '__main__':
    sys.exit(main())
