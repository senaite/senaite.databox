# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.DATABOX
#
# Copyright 2018 by it's authors.

from bika.lims import _
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implements


class IDataBox(model.Schema):
    """The DataBox container
    """

    # N.B. do not name this field `portal_type`
    query_type = schema.Choice(
        title=_(u"Query Type"),
        description=_(u"The type to query"),
        source="senaite.databox.vocabularies.addable_types",
        required=True,
    )


class DataBox(Item):
    """Intelligent Query Folder
    """
    implements(IDataBox)
