#!/usr/bin/env python

from __future__ import print_function

import argparse
from collections import defaultdict
import sys

import haproxystats


class SensuCheckStatus:
    RETURN_CODES = {'OK': 0, 'WARNING': 1, 'CRITICAL': 2, 'UNKNOWN': 3}
    status = RETURN_CODES['OK']

    def update_status(self, new_status, message):
        if self.RETURN_CODES[new_status] > self.status:
            self.status = self.RETURN_CODES[new_status]
        print('{}: {}'.format(new_status, message))


def get_haproxy_services_up_count_for_backends(base_url_path, username=None, password=None, backends=None):
    hs = haproxystats.HAProxyServer(base_url_path, username, password)
    found_backend_stats = defaultdict(dict)
    for listener in hs.listeners:  # a list of services found
        if not backends or listener.pxname in backends:
            backend = found_backend_stats[listener.pxname]
            if 'count' not in backend:
                backend['count'] = 0
                backend['up_count'] = 0
            backend['count'] += 1
            if 'UP' in listener.status:
                backend['up_count'] += 1
    return found_backend_stats


def check_haproxy_up_rates(
        base_url_path, username=None, password=None, backends=None, warning_percent=0.9, critical_percent=0.6,
        warning_down=None, critical_down=None):
    sensu_status = SensuCheckStatus()
    try:
        found_backend_stats = get_haproxy_services_up_count_for_backends(base_url_path, username, password, backends)
    except Exception as ex:
        sensu_status.update_status('UNKNOWN', 'Unknown exception: {}'.format(str(ex)))
        return sensu_status.status

    if backends and len(found_backend_stats.keys()) != len(backends):
        # Critial, there is a backend not found that was explicitly listed to monitor
        missing_backends = set(backends) - set(found_backend_stats.keys())
        sensu_status.update_status('CRITICAL', 'There are missing backends that were requested to be monitored: {}'.format(missing_backends))

    for backend_name in found_backend_stats:
        backend = found_backend_stats[backend_name]
        up_percent = float(backend['up_count']) / backend['count']
        down_count = backend['count'] - backend['up_count']
        if up_percent < critical_percent:
            sensu_status.update_status(
                'CRITICAL',
                'Backend {} has a critical percentage of services up ({}%)'.format(backend_name, int(up_percent * 100)))
        elif up_percent < warning_percent:
            sensu_status.update_status(
                'WARNING',
                'Backend {} has a warning percentage of services up ({}%)'.format(backend_name, int(up_percent * 100)))
        if critical_down and down_count >= critical_down:
            sensu_status.update_status(
                'CRITICAL',
                'Backend {} has a critical number of services down ({})'.format(backend_name, down_count))
        elif warning_down and down_count >= warning_down:
            sensu_status.update_status(
                'WARNING',
                'Backend {} has a warning number of services down ({})'.format(backend_name, down_count))

    return sensu_status.status


def _get_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--base-url-path", default="127.0.0.1/haproxy/stats")
    parser.add_argument("--username", help="Username to login to haproxy stats page.")
    parser.add_argument("--password", help="Password to login to haproxy stats page.")
    parser.add_argument(
        "--backend", dest="backends", action="append", default=[],
        help="Backend to check up percent. Defaults to all backends")
    parser.add_argument(
        "--warning-percent", type=float, default=0.9,
        help="Up percentage (non-inclusive), below which we should throw warning.")
    parser.add_argument(
        "--critical-percent", type=float, default=0.6,
        help="Up percentage (non-inclusive), below which we should throw critical.")
    parser.add_argument(
        "--warning-down", type=int, help="Down count at or above which we should throw warning.")
    parser.add_argument(
        "--critical-down", type=int, help="Down count at or above which we should throw critical.")
    return parser


def main():
    """Parser user input and execute the check.

    :return: Exit code (depending on severity).
    :rtype: :py:class:`int`
    """
    parser = _get_parser()
    args = parser.parse_args()
    rc = check_haproxy_up_rates(
        base_url_path=args.base_url_path,
        username=args.username,
        password=args.password,
        backends=args.backends,
        warning_percent=args.warning_percent,
        critical_percent=args.critical_percent,
        warning_down=args.warning_down,
        critical_down=args.critical_down,
    )
    return rc


if __name__ == '__main__':
    sys.exit(main())
