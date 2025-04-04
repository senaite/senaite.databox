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

from bika.lims import api
from senaite.databox.behaviors.databox import IDataBoxBehavior
from senaite.databox.config import NON_QUERYABLE_TYPES
from senaite.databox.config import DATE_INDEX_TYPES
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class IndexesVocabulary(object):
    """Returns all available indexes
    """
    def __call__(self, context):
        # XXX Workaround for missing context in nested choice widget vocabulary
        if context is None:
            # fetch context from the request
            request = api.get_request()
            if request and request["PARENTS"]:
                context = request["PARENTS"][0]
        items = []
        adapted = IDataBoxBehavior(context, None)
        if adapted is None:
            return SimpleVocabulary.fromValues([])
        catalog = adapted.get_catalog_tool()
        indexes = catalog.getIndexObjects()
        for index in indexes:
            name = index.getId()
            items.append(SimpleTerm(name, token=name, title=name))
        return SimpleVocabulary(items)


IndexesVocabularyFactory = IndexesVocabulary()


@implementer(IVocabularyFactory)
class DateIndexesVocabulary(object):
    """Returns all available date indexes
    """
    def __call__(self, context):
        items = []
        adapted = IDataBoxBehavior(context, None)
        if adapted is None:
            return SimpleVocabulary.fromValues([])

        catalog = adapted.get_catalog_tool()
        indexes = catalog.getIndexObjects()
        for index in indexes:
            if index.meta_type not in DATE_INDEX_TYPES:
                continue
            name = index.getId()
            items.append(SimpleTerm(name, token=name, title=name))
        return SimpleVocabulary(items)


DateIndexesVocabularyFactory = DateIndexesVocabulary()


@implementer(IVocabularyFactory)
class DisplayColumnsVocabulary(object):
    """Returns all available fields of the selected type
    """
    def __call__(self, context):
        # XXX Workaround for missing context in nested choice widget vocabulary
        if context is None:
            # fetch context from the request
            request = api.get_request()
            if request and request["PARENTS"]:
                context = request["PARENTS"][0]
        items = []
        adapted = IDataBoxBehavior(context, None)
        if adapted is None:
            return SimpleVocabulary.fromValues([])
        for field in adapted.get_fields():
            items.append(SimpleTerm(field, token=field, title=field))
        return SimpleVocabulary(items)


DisplayColumnsVocabularyFactory = DisplayColumnsVocabulary()


@implementer(IVocabularyFactory)
class QueryTypesVocabulary(object):

    def __call__(self, context):
        portal_state = api.get_view("plone_portal_state")
        content_types = portal_state.friendly_types()
        # filter out non queryable types
        content_types = filter(
            lambda pt: pt not in NON_QUERYABLE_TYPES, content_types)
        items = [
            SimpleTerm(item, item, item)
            for item in content_types
        ]
        return SimpleVocabulary(items)


QueryTypesVocabularyFactory = QueryTypesVocabulary()
