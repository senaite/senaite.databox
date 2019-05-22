# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.DATABOX
#
# Copyright 2018 by it's authors.

from plone.dexterity.content import Container
from plone.supermodel import model
from senaite.databox import senaiteMessageFactory as _
from zope import schema
from zope.interface import implements


class IDataBoxFolder(model.Schema):
    """A Folder for DataBoxes
    """

    title = schema.TextLine(
        title=_(u"Title"),
        description=_(u"Title of the Folder"),
        required=True,
    )


class DataBoxFolder(Container):
    """A Folder for DataBoxes
    """
    implements(IDataBoxFolder)
