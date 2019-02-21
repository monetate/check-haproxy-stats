#!/usr/bin/env python

import haproxystats
import time


def get_request_stats(backend, base_url_path="127.0.0.1/haproxy/stats", username="", password=""):
    """Return tuple of number of requests with (1xx, 2xx, 3xx, 4xx, 5xx, other response codes).

    :return: (number of requests with 1xx, 2xx, 3xx, 4xx, 5xx, other response codes)
    :rtype: :py:class:`tuple(int, int, int, int, int, int)`
    """
    h = haproxystats.HAProxyServer(base_url_path, username, password)
    sums = (0, 0, 0, 0, 0, 0)
    matched = False
    for b in h.backends:
        if not b.name.startswith(backend):
            continue
        sums = tuple(map(sum, zip(sums, (b.hrsp_1xx, b.hrsp_2xx, b.hrsp_3xx, b.hrsp_4xx, b.hrsp_5xx, b.hrsp_other))))
        matched = True
    if not matched:
        raise ValueError("Did not find {0} backend".format(backend))
    else:
        return sums


def get_hrsp_5xx_ratio(backend, base_url_path, username, password, interval):
    """Return ratio of requests that has 5xx code during specified interval seconds.

    :return: Ratio of requests that have 5xx HTTP codes
    :rtype: :py:class:`float`
    """
    requests_initial = get_request_stats(backend, base_url_path, username, password)
    time.sleep(interval)
    requests_final = get_request_stats(backend, base_url_path, username, password)

    total_requests_during_interval = sum(requests_final) - sum(requests_initial)
    hrsp_5xx_during_interval = requests_final[4] - requests_initial[4]

    # division by zero avoidance
    if total_requests_during_interval == 0:
        hrsp_5xx_ratio_interval = 0.00
    else:
        hrsp_5xx_ratio_interval = float(hrsp_5xx_during_interval) / total_requests_during_interval

    return hrsp_5xx_ratio_interval
