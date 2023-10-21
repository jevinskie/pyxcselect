#!/usr/bin/env python3

import sys

from setuptools import setup

if sys.platform != "darwin":
    sys.exit("Error: This package is only supported on macOS.")

setup()
