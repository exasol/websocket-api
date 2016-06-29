#!/usr/bin/env python

import re
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='EXASOL WS API',
    long_description="EXASOL Python DB API 2",
    version="0.0.1",
    license="N/A",
    maintainer="Oleksandr Kozachuk",
    maintainer_email="oleksandr.kozachuk@exasol.com",
    description="EXASOL Python DB API 2.",
    url='https://github.com/EXASOL/websocket-api',
    packages=[
        'EXASOL',
    ],
    install_requires=[
        'websocket_client',
        'rsa',
    ]
)
