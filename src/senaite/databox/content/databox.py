# -*- coding: utf-8 -*-

from plone.dexterity.content import Item
from senaite.databox.interfaces import IDataBox
from zope.interface import implementer


@implementer(IDataBox)
class DataBox(Item):
    """Intelligent Query Folder
    """
