# -*- coding: utf-8 -*-

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
