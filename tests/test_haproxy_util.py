#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `haproxy_util` module."""
import unittest

from mock import Mock, PropertyMock, patch
import check_haproxy_stats.haproxy_util


class TestHaProxy_Util(unittest.TestCase):

    """Test cases for haproxy_util."""

    def test_get_request_stats_no_traffic(self):
        """Test scenario where we receive no traffic at all."""
        with patch("haproxystats.HAProxyServer") as haproxy_server_instance:
            check_trk_backend = Mock(hrsp_1xx=0, hrsp_2xx=0, hrsp_3xx=0, hrsp_4xx=0, hrsp_5xx=0, hrsp_other=0)
            type(check_trk_backend).name = PropertyMock(return_value="check-trk")  # "name" is special
            haproxy_server = Mock(backends=[check_trk_backend])
            haproxy_server_instance.return_value = haproxy_server

            result = check_haproxy_stats.haproxy_util.get_request_stats(
                base_url_path="127.0.0.1/haproxy/stats", username="someone", password="password", backend="check-trk")
            expected_result = (0, 0, 0, 0, 0, 0)
            self.assertEqual(result, expected_result)

    def test_get_request_stats_some_traffic(self):
        """Test scenario where we receive various traffic resulting in some {1,2,3,4,5, other}xx codes."""
        with patch("haproxystats.HAProxyServer") as haproxy_server_instance:
            check_trk_backend = Mock(hrsp_1xx=1, hrsp_2xx=2, hrsp_3xx=3, hrsp_4xx=4, hrsp_5xx=5, hrsp_other=0)
            type(check_trk_backend).name = PropertyMock(return_value="check-trk")  # "name" is special
            haproxy_server = Mock(backends=[check_trk_backend])
            haproxy_server_instance.return_value = haproxy_server

            result = check_haproxy_stats.haproxy_util.get_request_stats(
                base_url_path="127.0.0.1/haproxy/stats", username="someone", password="password", backend="check-trk")
            expected_result = (1, 2, 3, 4, 5, 0)
            self.assertEqual(result, expected_result)

    def test_get_hrsp_5xx_ratio_no_traffic(self):
        """Test scenario where we do not receive any traffic at all."""
        with patch("check_haproxy_stats.haproxy_util.get_request_stats") as get_request_stats:
            get_request_stats.side_effect = [(0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0)]
            r = check_haproxy_stats.haproxy_util.get_hrsp_5xx_ratio(
                backend="check-trk",
                base_url_path="127.0.0.1/haproxy/stats",
                username="someone",
                password="password",
                interval=0)
            self.assertEqual(r, 0.0)

    def test_get_hrsp_5xx_ratio_no_traffic_during_interval(self):
        """Test scenario where we do not receive any traffic at all."""
        with patch("check_haproxy_stats.haproxy_util.get_request_stats") as get_request_stats:
            get_request_stats.side_effect = [(1, 1, 1, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1, 1, 1)]
            r = check_haproxy_stats.haproxy_util.get_hrsp_5xx_ratio(
                backend="check-trk",
                base_url_path="127.0.0.1/haproxy/stats",
                username="someone",
                password="password",
                interval=0)
            self.assertEqual(r, 0.0)

    def test_get_hrsp_5xx_ratio_some_traffic_all_500(self):
        """Test scenario where we receive all traffic to be 500."""
        with patch("check_haproxy_stats.haproxy_util.get_request_stats") as get_request_stats:
            get_request_stats.side_effect = [(0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 1, 0)]
            r = check_haproxy_stats.haproxy_util.get_hrsp_5xx_ratio(
                backend="check-trk",
                base_url_path="127.0.0.1/haproxy/stats",
                username="someone",
                password="password",
                interval=0)
            self.assertEqual(r, 1.0)

    def test_get_hrsp_5xx_ratio_some_traffic_half_500(self):
        """Test scenario where we receive half of traffic resulting in 5xx HTTP code."""
        with patch("check_haproxy_stats.haproxy_util.get_request_stats") as get_request_stats:
            get_request_stats.side_effect = [(0, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 0)]
            r = check_haproxy_stats.haproxy_util.get_hrsp_5xx_ratio(
                backend="check-trk",
                base_url_path="127.0.0.1/haproxy/stats",
                username="someone",
                password="password",
                interval=0)
            self.assertEqual(r, 0.5)
