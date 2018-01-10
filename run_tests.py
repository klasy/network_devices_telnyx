#!/usr/bin/env python

from unittest import TestLoader, TextTestRunner

loader = TestLoader()
start_dir = 'test/'
suite = loader.discover(start_dir)

TextTestRunner(verbosity=2).run(suite)