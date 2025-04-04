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

from datetime import datetime

import six

from bika.lims import api
from bika.lims.utils import get_link
from DateTime import DateTime
from plone.protect.utils import addTokenToUrl
from Products.ATContentTypes.utils import DT2dt

LINK_TO_PARENT_TYPES = [
    "Analysis",
]


def to_string(obj, key, value, **kw):
    """to string
    """
    if isinstance(value, six.string_types):
        value = api.safe_unicode(value).encode("utf-8")
    if value is None:
        value = ""
    return str(value)


def to_link(obj, key, value, **kw):
    """to link
    """
    value = to_string(obj, key, value)
    if not value:
        return ""
    if api.get_portal_type(obj) in LINK_TO_PARENT_TYPES:
        obj = api.get_parent(obj)
    url = addTokenToUrl(api.get_url(obj))
    return get_link(url, value)


def to_date(obj, key, value, dfmt="%d.%m.%Y"):
    """to date
    """
    if isinstance(value, DateTime):
        return DT2dt(value).strftime(dfmt)
    elif isinstance(value, datetime):
        return value.strftime(dfmt)
    return value


def to_long_date(obj, key, value, dfmt="%d.%m.%Y %H:%M"):
    """to long date
    """
    return to_date(obj, key, value, dfmt=dfmt)
