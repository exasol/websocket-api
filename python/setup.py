#!/usr/bin/env python

import re
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='EXASOL DB API',
    version="6.0.0",
    license="MIT",
    maintainer="Oleksandr Kozachuk",
    maintainer_email="support@exasol.com",
    description="EXASOL Python DB API v2.0 compatible native driver",
    long_description="EXASOL Python DB API v2.0 compatible native driver based ond Websockets API for communication and JSON for serialization.",
    url='https://github.com/EXASOL/websocket-api',
    packages=[
        'EXASOL',
    ],
    install_requires=[
        'websocket_client',
        'rsa',
    ]
)
