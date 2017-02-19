#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "haproxy-stats",
    "future",
]

test_requirements = [
]

setup(
    name='check_haproxy_stats',
    version='2.0.0',
    description="Check HAProxy related statistics",
    long_description=readme + '\n\n' + history,
    author="Monetate, Inc.",
    author_email='devops@monetate.com',
    url='https://github.com/monetate/check_haproxy_stats',
    packages=[
        'check_haproxy_stats',
    ],
    package_dir={'check_haproxy_stats':
                 'check_haproxy_stats'},
    entry_points={
        'console_scripts': [
            "check-haproxy-stats-5xx = check_haproxy_stats.check_haproxy_stats_5xx:main",
            "metrics-haproxy-stats-5xx = check_haproxy_stats.metrics_haproxy_stats_5xx:main",
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='check_haproxy_stats',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
