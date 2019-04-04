#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `check_haproxy_stats_5xx` module."""
import sys
import unittest

from check_haproxy_stats import check_haproxy_stats_up
from mock import patch


class TestCheck_haproxy_stats_up(unittest.TestCase):
    """Test cases for check_haproxy_stats_up."""

    def test_check_haproxy_percents_test_ok(self):
        """
        Test 0.90 up percent with warning ratio and critical ratio of 0.90 and 0.60.

        check_haproxy_up_rates should return OK code.
        """
        with patch("check_haproxy_stats.check_haproxy_stats_up.get_haproxy_services_up_count_for_backends") as get_backend_counts:
            get_backend_counts.return_value = {
                'backend-1': {
                    'count': 2,
                    'up_count': 2,
                },
                'backend-2': {
                    'count': 100,
                    'up_count': 90,  # below 90% will cause percent down warning
                }
            }
            r = check_haproxy_stats_up.check_haproxy_up_rates(
                base_url_path="127.0.0.1/haproxy/stats",
                warning_percent=0.90,
                critical_percent=0.60,
                )
            self.assertEqual(r, check_haproxy_stats_up.SensuCheckStatus.RETURN_CODES["OK"])

    def test_check_haproxy_percents_test_warn(self):
        """
        Test 0.75 and 0.90 up percent with warning ratio and critical ratio of 0.90 and 0.60.

        check_haproxy_up_rates should return WARNING code.
        """
        with patch("check_haproxy_stats.check_haproxy_stats_up.get_haproxy_services_up_count_for_backends") as get_backend_counts:
            get_backend_counts.return_value = {
                'backend-1': {
                    'count': 4,
                    'up_count': 3,  # 75% will cause a warning
                },
                'backend-2': {
                    'count': 100,
                    'up_count': 90,  # below 90% will cause percent down warning
                }
            }
            r = check_haproxy_stats_up.check_haproxy_up_rates(
                base_url_path="127.0.0.1/haproxy/stats",
                warning_percent=0.90,
                critical_percent=0.60,
                )
            self.assertEqual(r, check_haproxy_stats_up.SensuCheckStatus.RETURN_CODES["WARNING"])

    def test_check_haproxy_percents_test_critical(self):
        """
        Test 0.50 and .61 up percent with warning ratio and critical ratio of 0.90 and 0.60.

        check_haproxy_up_rates should return CRITICAL code.
        """
        with patch("check_haproxy_stats.check_haproxy_stats_up.get_haproxy_services_up_count_for_backends") as get_backend_counts:
            get_backend_counts.return_value = {
                'backend-1': {
                    'count': 4,
                    'up_count': 2,  # 50% will cause a critical
                },
                'backend-2': {
                    'count': 100,
                    'up_count': 61,  # below 61% will cause percent down warning
                }
            }
            r = check_haproxy_stats_up.check_haproxy_up_rates(
                base_url_path="127.0.0.1/haproxy/stats",
                warning_percent=0.90,
                critical_percent=0.60,
                )
            self.assertEqual(r, check_haproxy_stats_up.SensuCheckStatus.RETURN_CODES["CRITICAL"])

    def test_check_haproxy_down_test_ok(self):
        """
        Test 0 down return OK

        check_haproxy_up_rates should return OK code.
        """
        with patch("check_haproxy_stats.check_haproxy_stats_up.get_haproxy_services_up_count_for_backends") as get_backend_counts:
            get_backend_counts.return_value = {
                'backend-1': {
                    'count': 2,
                    'up_count': 2,
                },
                'backend-2': {
                    'count': 100,
                    'up_count': 100,
                }
            }
            r = check_haproxy_stats_up.check_haproxy_up_rates(
                base_url_path="127.0.0.1/haproxy/stats",
                warning_percent=0.10,
                critical_percent=0.10,
                warning_down=1,
                critical_down=16,
                )
            self.assertEqual(r, check_haproxy_stats_up.SensuCheckStatus.RETURN_CODES["OK"])

    def test_check_haproxy_down_test_warn(self):
        """
        Test 10 down on one backend and 1 down on another backend causes warning >= 1 down

        check_haproxy_up_rates should return WARNING code.
        """
        with patch("check_haproxy_stats.check_haproxy_stats_up.get_haproxy_services_up_count_for_backends") as get_backend_counts:
            get_backend_counts.return_value = {
                'backend-1': {
                    'count': 2,
                    'up_count': 1,
                },
                'backend-2': {
                    'count': 100,
                    'up_count': 90,
                }
            }
            r = check_haproxy_stats_up.check_haproxy_up_rates(
                base_url_path="127.0.0.1/haproxy/stats",
                warning_percent=0.10,
                critical_percent=0.10,
                warning_down=1,
                critical_down=16,
                )
            self.assertEqual(r, check_haproxy_stats_up.SensuCheckStatus.RETURN_CODES["WARNING"])

    def test_check_haproxy_down_test_critical(self):
        """
        Test 25 down on one backend and 1 down on another backend causes critical >= 16 down

        check_haproxy_up_rates should return CRITICAL code.
        """
        with patch("check_haproxy_stats.check_haproxy_stats_up.get_haproxy_services_up_count_for_backends") as get_backend_counts:
            get_backend_counts.return_value = {
                'backend-1': {
                    'count': 2,
                    'up_count': 1,
                },
                'backend-2': {
                    'count': 100,
                    'up_count': 75,
                }
            }
            r = check_haproxy_stats_up.check_haproxy_up_rates(
                base_url_path="127.0.0.1/haproxy/stats",
                warning_percent=0.10,
                critical_percent=0.10,
                warning_down=1,
                critical_down=16,
                )
            self.assertEqual(r, check_haproxy_stats_up.SensuCheckStatus.RETURN_CODES["CRITICAL"])

    def test_check_haproxy_percents_for_backend_test_ok(self):
        """
        Test backend-1 check only tests backend-1 up percent with warning ratio and critical ratio of 0.90 and 0.60.

        check_haproxy_up_rates should return OK code.
        """
        with patch("check_haproxy_stats.check_haproxy_stats_up.get_haproxy_services_up_count_for_backends") as get_backend_counts:
            get_backend_counts.return_value = {
                'backend-1': {
                    'count': 2,
                    'up_count': 2,
                },
                'backend-2': {
                    'count': 100,
                    'up_count': 3,
                }
            }
            r = check_haproxy_stats_up.check_haproxy_up_rates(
                base_url_path="127.0.0.1/haproxy/stats",
                warning_percent=0.90,
                critical_percent=0.60,
                backends=['backend-1', ]
                )
            self.assertEqual(r, check_haproxy_stats_up.SensuCheckStatus.RETURN_CODES["OK"])

    def test_check_haproxy_critical_if_backend_not_found(self):
        """
        Test CRITICAL if backend in check list not found

        check_haproxy_up_rates should return CRITICAL code.
        """
        with patch("check_haproxy_stats.check_haproxy_stats_up.get_haproxy_services_up_count_for_backends") as get_backend_counts:
            get_backend_counts.return_value = {
                'backend-1': {
                    'count': 2,
                    'up_count': 2,
                },
                'backend-2': {
                    'count': 100,
                    'up_count': 90,  # below 90% will cause percent down warning
                }
            }
            r = check_haproxy_stats_up.check_haproxy_up_rates(
                base_url_path="127.0.0.1/haproxy/stats",
                warning_percent=0.90,
                critical_percent=0.60,
                backends=['backend-1', 'no-such-backend', ]
                )
            self.assertEqual(r, check_haproxy_stats_up.SensuCheckStatus.RETURN_CODES["CRITICAL"])
