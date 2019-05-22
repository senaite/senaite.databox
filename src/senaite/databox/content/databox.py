# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.DATABOX
#
# Copyright 2018 by it's authors.

from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implements


class IDataBox(model.Schema):
    """The DataBox container
    """


class DataBox(Item):
    """Intelligent Query Folder
    """
    implements(IDataBox)
