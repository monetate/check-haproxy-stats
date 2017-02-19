#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `check_haproxy_stats_5xx` module."""
import sys
import unittest

from check_haproxy_stats import check_haproxy_stats_5xx
from mock import patch


class TestCheck_haproxy_stats_5xx(unittest.TestCase):

    """Test cases for check_haproxy_stats_5xx."""

    def test_handle_ok_exit_code(self):
        """Test typical OK exit code."""
        rc = check_haproxy_stats_5xx._handle_ok(
            backend="check-trk", hrsp_5xx_ratio=0.00, warning_ratio=0.01, critical_ratio=0.02, interval=60)
        self.assertEqual(rc, check_haproxy_stats_5xx.RETURN_CODES["OK"])

    def test_handle_warning_exit_code(self):
        """Test typical warning exit code."""
        rc = check_haproxy_stats_5xx._handle_warning(
            backend="check-trk", hrsp_5xx_ratio=0.015, warning_ratio=0.01, critical_ratio=0.02, interval=60)
        self.assertEqual(rc, check_haproxy_stats_5xx.RETURN_CODES["WARNING"])

    def test_handle_critical_exit_code(self):
        """Test typical critical exit code."""
        rc = check_haproxy_stats_5xx._handle_critical(
            backend="check-trk", hrsp_5xx_ratio=0.021, warning_ratio=0.01, critical_ratio=0.02, interval=60)
        self.assertEqual(rc, check_haproxy_stats_5xx.RETURN_CODES["CRITICAL"])

    def test_handle_unknown_exit_code(self):
        """Test typical unknown exit code."""
        rc = check_haproxy_stats_5xx._handle_unknown(exception_message="Some unknown exception message")
        self.assertEqual(rc, check_haproxy_stats_5xx.RETURN_CODES["UNKNOWN"])

    # def test_get_request_stats_no_traffic(self):
    #     """Test scenario where we receive no traffic at all."""
    #     with patch("haproxystats.HAProxyServer") as haproxy_server_instance:
    #         check_trk_backend = Mock(hrsp_1xx=0, hrsp_2xx=0, hrsp_3xx=0, hrsp_4xx=0, hrsp_5xx=0, hrsp_other=0)
    #         type(check_trk_backend).name = PropertyMock(return_value="check-trk")  # "name" is special
    #         haproxy_server = Mock(backends=[check_trk_backend])
    #         haproxy_server_instance.return_value = haproxy_server

    #         result = check_haproxy_stats_5xx._get_request_stats(
    #             base_url_path="127.0.0.1/haproxy/stats", username="someone", password="password", backend="check-trk")
    #         expected_result = (0, 0)
    #         self.assertEqual(result, expected_result)

    # def test_get_request_stats_some_traffic(self):
    #     """Test scenario where we receive various traffic resulting in some {1,2,3,4,5}xx codes."""
    #     with patch("haproxystats.HAProxyServer") as haproxy_server_instance:
    #         check_trk_backend = Mock(hrsp_1xx=1, hrsp_2xx=2, hrsp_3xx=3, hrsp_4xx=4, hrsp_5xx=5, hrsp_other=0)
    #         type(check_trk_backend).name = PropertyMock(return_value="check-trk")  # "name" is special
    #         haproxy_server = Mock(backends=[check_trk_backend])
    #         haproxy_server_instance.return_value = haproxy_server

    #         result = check_haproxy_stats_5xx._get_request_stats(
    #             base_url_path="127.0.0.1/haproxy/stats", username="someone", password="password", backend="check-trk")
    #         expected_result = (15, 5)
    #         self.assertEqual(result, expected_result)

    # def test_get_hrsp_5xx_ratio_no_traffic(self):
    #     """Test scenario where we do not receive any traffic at all."""
    #     with patch("check_haproxy_stats.haproxy_util.get_request_stats") as get_request_stats:
    #         get_request_stats.side_effect = [(0, 0, 0 , 0, 0, 0), (0, 0, 0, 0, 0, 0)]
    #         r = check_haproxy_stats_5xx._get_hrsp_5xx_ratio(
    #             backend="check-trk",
    #             base_url_path="127.0.0.1/haproxy/stats",
    #             username="someone",
    #             password="password",
    #             interval=0)
    #         self.assertEqual(r, 0.0)

    # def test_get_hrsp_5xx_ratio_no_traffic_during_interval(self):
    #     """Test scenario where we do not receive any traffic at all."""
    #     with patch("check_haproxy_stats.haproxy_util.get_request_stats") as get_request_stats:
    #         get_request_stats.side_effect = [(1, 1, 1, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1, 1, 1)]
    #         r = check_haproxy_stats_5xx._get_hrsp_5xx_ratio(
    #             backend="check-trk",
    #             base_url_path="127.0.0.1/haproxy/stats",
    #             username="someone",
    #             password="password",
    #             interval=0)
    #         self.assertEqual(r, 0.0)

    # def test_get_hrsp_5xx_ratio_some_traffic_all_500(self):
    #     """Test scenario where we receive all traffic to be 500."""
    #     with patch("check_haproxy_stats.haproxy_util.get_request_stats") as get_request_stats:
    #         get_request_stats.side_effect = [(0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 1, 0)]
    #         r = check_haproxy_stats_5xx._get_hrsp_5xx_ratio(
    #             backend="check-trk",
    #             base_url_path="127.0.0.1/haproxy/stats",
    #             username="someone",
    #             password="password",
    #             interval=0)
    #         self.assertEqual(r, 1.0)

    # def test_get_hrsp_5xx_ratio_some_traffic_half_500(self):
    #     """Test scenario where we receive half of traffic resulting in 5xx HTTP code."""
    #     with patch("check_haproxy_stats.haproxy_util.get_request_stats") as get_request_stats:
    #         get_request_stats.side_effect = [(0, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 0)]
    #         r = check_haproxy_stats_5xx._get_hrsp_5xx_ratio(
    #             backend="check-trk",
    #             base_url_path="127.0.0.1/haproxy/stats",
    #             username="someone",
    #             password="password",
    #             interval=0)
    #         self.assertEqual(r, 0.5)

    def test_check_haproxy_rates_test_ok(self):
        """
        Test 0.0 failure rate with warning ratio and critical ratio of 0.01 and 0.02.

        _check_haproxy_rates should return OK code.
        """
        with patch("check_haproxy_stats.haproxy_util.get_hrsp_5xx_ratio") as get_hrsp_5xx_ratio:
            get_hrsp_5xx_ratio.return_value = 0.00
            r = check_haproxy_stats_5xx._check_haproxy_rates(
                backend="check-trk",
                warning_ratio=0.01,
                critical_ratio=0.02,
                base_url_path="127.0.0.1/haproxy/stats",
                username="someone",
                password="someone",
                interval=1)
            self.assertEqual(r, check_haproxy_stats_5xx.RETURN_CODES["OK"])

    def test_check_haproxy_rates_test_warn(self):
        """
        Test 0.015 failure rate with warning ratio and critical ratio of 0.01 and 0.02.

        _check_haproxy_rates should return WARNING.
        """
        with patch("check_haproxy_stats.haproxy_util.get_hrsp_5xx_ratio") as get_hrsp_5xx_ratio:
            get_hrsp_5xx_ratio.return_value = 0.015
            r = check_haproxy_stats_5xx._check_haproxy_rates(
                backend="check-trk",
                warning_ratio=0.01,
                critical_ratio=0.02,
                base_url_path="127.0.0.1/haproxy/stats",
                username="someone",
                password="someone",
                interval=1)
            self.assertEqual(r, check_haproxy_stats_5xx.RETURN_CODES["WARNING"])

    def test_check_haproxy_rates_test_critical(self):
        """Test 0.015 failure rate with warning ratio and critical ratio of 0.01 and 0.02.

        _check_haproxy_rates should return CRITICAL.
        """
        with patch("check_haproxy_stats.haproxy_util.get_hrsp_5xx_ratio") as get_hrsp_5xx_ratio:
            get_hrsp_5xx_ratio.return_value = 0.021
            r = check_haproxy_stats_5xx._check_haproxy_rates(
                backend="check-trk",
                warning_ratio=0.01,
                critical_ratio=0.02,
                base_url_path="127.0.0.1/haproxy/stats",
                username="someone",
                password="someone",
                interval=1)
            self.assertEqual(r, check_haproxy_stats_5xx.RETURN_CODES["CRITICAL"])

    def test_check_haproxy_rates_test_unknown(self):
        """Test we ran into an unknown issue (ValueError), _check_haproxy_rates should return UNKNOWN code."""
        with patch("check_haproxy_stats.haproxy_util.get_hrsp_5xx_ratio") as get_hrsp_5xx_ratio:
            get_hrsp_5xx_ratio.side_effect = ValueError("check-trk backend cannot be found")
            r = check_haproxy_stats_5xx._check_haproxy_rates(
                backend="check-trk",
                warning_ratio=0.01,
                critical_ratio=0.02,
                base_url_path="127.0.0.1/haproxy/stats",
                username="someone",
                password="someone",
                interval=1)
            self.assertEqual(r, check_haproxy_stats_5xx.RETURN_CODES["UNKNOWN"])

    def test_parser(self):
        """Test typical use of _get_parser()."""
        parser = check_haproxy_stats_5xx._get_parser()
        args = parser.parse_args(
            ["--backend", "check-trk", "--warning-ratio", "0.01", "--critical-ratio", "0.02", "--base-url-path",
             "some-url-path", "--username", "someone", "--password", "password", "--interval", "120"])
        self.assertEqual(args.backend, "check-trk")
        self.assertEqual(args.warning_ratio, 0.01)
        self.assertEqual(args.critical_ratio, 0.02)
        self.assertEqual(args.base_url_path, "some-url-path")
        self.assertEqual(args.username, "someone")
        self.assertEqual(args.password, "password")
        self.assertEqual(args.interval, 120)

    def test_main(self):
        """Test typical use of main()."""
        simulated_check = ["check-haproxys-stats-5xx", "--backend", "check-trk", "--warning-ratio", "0.01",
                           "--critical-ratio", "0.02", "--base-url-path", "some-url-path", "--username", "someone",
                           "--password", "password", "--interval", "120"]
        check_haproxy_stats = "check_haproxy_stats.check_haproxy_stats_5xx._check_haproxy_rates"
        with patch.object(sys, "argv", simulated_check), patch(check_haproxy_stats) as check_haproxy_rates:

            check_haproxy_stats_5xx.main()
            check_haproxy_rates.assert_called_with(
                backend="check-trk",
                warning_ratio=0.01,
                critical_ratio=0.02,
                base_url_path="some-url-path",
                username="someone",
                password="password",
                interval=120)
