#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `check_haproxy_stats_5xx` module."""
import sys
import unittest

from check_haproxy_stats import metrics_haproxy_stats_5xx
from mock import patch


class TestMetrics_Haproxy_Stats_5xx(unittest.TestCase):

    """Test cases for metrics_haproxy_stats_5xx."""

    def test_parser(self):
        """Test typical use of _get_parser()."""
        parser = metrics_haproxy_stats_5xx._get_parser()
        args = parser.parse_args(["--backend", "check-trk", "--base-url-path", "some-url-path", "--gmetric-path",
                                  "/usr/local/bin/gmetric", "--gmetric-tmax", "1", "--gmetric-dmax", "2", "--username",
                                  "someone", "--password", "password", "--interval", "120"])
        self.assertEqual(args.backend, "check-trk")
        self.assertEqual(args.base_url_path, "some-url-path")
        self.assertEqual(args.username, "someone")
        self.assertEqual(args.password, "password")
        self.assertEqual(args.interval, 120)
        self.assertEqual(args.gmetric_path, "/usr/local/bin/gmetric")
        self.assertEqual(args.gmetric_tmax, 1)
        self.assertEqual(args.gmetric_dmax, 2)

    @patch("check_haproxy_stats.haproxy_util.get_hrsp_5xx_ratio")
    @patch("subprocess.check_call")
    @patch("socket.gethostname")
    def test_report_haproxy_rates(self, socket_hostname, subprocess_check_call, get_hrsp_5xx_ratio):
        """Test typical case of report_haproxy_rates."""
        socket_hostname.return_value = "host"
        get_hrsp_5xx_ratio.return_value = 0.1
        metrics_haproxy_stats_5xx._report_haproxy_rates(
            backend="check-trk",
            base_url_path="some-url",
            username="username",
            password="password",
            interval=60,
            gmetric_path="/usr/bin/gmetric",
            gmetric_dmax=120,
            gmetric_tmax=60)
        subprocess_check_call.assert_called_with(["/usr/bin/gmetric", "-d", "120", "-x", "60", "-n",
                                                  "haproxy_host_check-trk_5xx_percent", "-v", "10.00", "-s", "both",
                                                  "-g", "haproxy", "-t", "float"])

    def test_main(self):
        """Test typical use of main()."""
        simulated_check = ["metrics-haproxy-stats-5xx", "--backend", "check-trk", "--base-url-path", "some-url-path",
                           "--gmetric-path", "/usr/local/bin/gmetric", "--gmetric-tmax", "1", "--gmetric-dmax", "2",
                           "--username", "someone", "--password", "password", "--interval", "120"]
        report_haproxy_rates = "check_haproxy_stats.metrics_haproxy_stats_5xx._report_haproxy_rates"
        with patch.object(sys, "argv", simulated_check), patch(report_haproxy_rates) as report_haproxy_rates_call:

            metrics_haproxy_stats_5xx.main()
            report_haproxy_rates_call.assert_called_with(
                backend="check-trk",
                base_url_path="some-url-path",
                username="someone",
                password="password",
                interval=120,
                gmetric_path="/usr/local/bin/gmetric",
                gmetric_dmax=2,
                gmetric_tmax=1)
