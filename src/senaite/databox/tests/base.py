# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.DATABOX.
#
# SENAITE.DATABOX is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2018-2025 by it's authors.
# Some rights reserved, see README and LICENSE.

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing.bbb_at import PloneTestCase
from plone.protect.authenticator import createToken
from senaite.databox.tests.layers import BASE_TESTING


class BaseTestCase(PloneTestCase):
    """Use for test cases which do not rely on the demo data
    """
    layer = BASE_TESTING

    def setUp(self):
        super(BaseTestCase, self).setUp()
        # Fixing CSRF protection
        # https://github.com/plone/plone.protect/#fixing-csrf-protection-failures-in-tests
        self.request = self.layer["request"]
        # Disable plone.protect for these tests
        self.request.form["_authenticator"] = createToken()
        # Eventuelly you find this also useful
        self.request.environ["REQUEST_METHOD"] = "POST"

        setRoles(self.portal, TEST_USER_ID, ["LabManager", "Manager"])

        # Default skin is set to "Sunburst Theme"!
        # => This causes an `AttributeError` when we want to access
        #    e.g. 'guard_handler' FSPythonScript
        self.portal.changeSkin("Plone Default")
