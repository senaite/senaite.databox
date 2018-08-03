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


class IDataBox(model.Schema):
    """The DataBox container
    """

    title = schema.TextLine(
        title=_(u"Title"),
        description=_(u"Please name your DataBox"),
        required=True,
    )

    portal_type = schema.Choice(
        title=_(u"Portal Type"),
        description=_(u"The portal type to query"),
        source="senaite.databox.vocabularies.addable_types",
        required=True,
    )


class DataBox(Container):
    """A configurable data container
    """
    implements(IDataBox)
