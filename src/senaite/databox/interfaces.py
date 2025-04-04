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

from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager


class ISenaiteDataBox(Interface):
    """The Add-on specific browser layer
    """


class IDataBoxFolder(Interface):
    """Explicit marker interface for DataBoxFolder
    """


class IDataBox(Interface):
    """Explicit marker interface for DataBox
    """


class IFieldConverter(Interface):
    """Marker interface for field converter utilities
    """


class IDataBoxJS(IViewletManager):
    """A viewlet manager that provides the JavaScripts for DataBox
    """
