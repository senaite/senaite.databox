# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.DATABOX
#
# Copyright 2018 by it's authors.

from plone.dexterity.content import Container
from senaite.databox.interfaces import IDataBoxFolder
from zope.interface import implementer


@implementer(IDataBoxFolder)
class DataBoxFolder(Container):
    """A Folder for DataBoxes
    """
