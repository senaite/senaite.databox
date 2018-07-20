# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.DATABOX
#
# Copyright 2018 by it's authors.

from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implements
from zope import schema
from senaite.databox import senaiteMessageFactory as _


class IDataBox(model.Schema):
    """The DataBox container
    """

    title = schema.TextLine(
        title=_(u"Title"),
        description=_(u"A short name that describes the Databox"),
        required=True,
    )


class DataBox(Container):
    """A configurable data container
    """
    implements(IDataBox)
