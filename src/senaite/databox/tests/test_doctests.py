# -*- coding: utf-8 -*-

import doctest
from os.path import join

from pkg_resources import resource_listdir

import unittest2 as unittest
from senaite.health.config import PROJECTNAME
from senaite.health.tests.base import BaseTestCase
from Testing import ZopeTestCase as ztc

# Option flags for doctests
flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF


def test_suite():
    suite = unittest.TestSuite()
    for doctestfile in get_doctest_files():
        suite.addTests([
            ztc.ZopeDocFileSuite(
                doctestfile,
                test_class=BaseTestCase,
                optionflags=flags
            )
        ])
    return suite


def get_doctest_files():
    """Returns a list with the doctest files
    """
    files = resource_listdir(PROJECTNAME, "tests/doctests")
    files = filter(lambda file_name: file_name.endswith(".rst"), files)
    return map(lambda file_name: join("doctests", file_name), files)
