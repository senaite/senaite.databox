# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.DATABOX
#
# Copyright 2018 by it's authors.

from zope.interface import Interface


class IDataBoxLayer(Interface):
    """The Add-on specific browser layer
    """


class IAutoGenerateID(Interface):
    """Auto-generate ID with ID server
    """
