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

import ast
from contextlib import contextmanager
from copy import copy
from datetime import datetime

import transaction
from bika.lims import api
from DateTime import DateTime
from dateutil import parser
from plone.app.z3cform.widget import DatetimeFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.utils import resolveDottedName
from plone.supermodel import model
from senaite.databox import _
from senaite.databox import logger
from senaite.databox.config import DATE_INDEX_TYPES
from senaite.databox.config import IGNORE_CATALOG_IDS
from senaite.databox.config import IGNORE_FIELDS
from senaite.databox.config import PARENT_TYPES
from senaite.databox.config import TMP_FOLDER_KEY
from senaite.databox.config import UID_CATALOG
from z3c.form.interfaces import IAddForm
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


class ParentField(object):
    def __init__(self, portal_type):
        self.type = "reference"
        self.name = "Parent"
        self.portal_type = portal_type


@provider(IFormFieldProvider)
class IDataBoxBehavior(model.Schema):

    # N.B. do not name this field `portal_type`
    query_type = schema.Choice(
        title=_(u"Query Type"),
        description=_(u"The type to query"),
        source="senaite.databox.vocabularies.query_types",
        required=True,
    )

    # directives.widget("columns", multiFieldWidgetFactory, klass=u"datagrid")
    directives.omitted(IAddForm, "columns")
    columns = schema.List(
        title=_(u"Columns"),
        value_type=schema.Dict(
            title=_(u"Column Config"),
            key_type=schema.Choice(
                title=_(u"Column"),
                source="senaite.databox.vocabularies.display_columns"),
            value_type=schema.Dict(
                key_type=schema.TextLine(title=u"Key"),
                value_type=schema.TextLine(title=u"Value"),
            ),
        ),
        required=False,
    )

    directives.omitted(IAddForm, "advanced_query")
    advanced_query = schema.Dict(
        title=_(u"Advanced Query"),
        key_type=schema.Choice(
            title=_(u"Query Index"),
            source="senaite.databox.vocabularies.indexes"),
        value_type=schema.TextLine(title=_("Query Value")),
        required=False,
    )

    directives.omitted(IAddForm, "date_index")
    date_index = schema.Choice(
        title=_(u"Query date index"),
        description=_(u"The date index to query"),
        source="senaite.databox.vocabularies.date_indexes",
        required=False,
        default="created",
    )

    directives.widget("date_from", DatetimeFieldWidget, klass=u"datepicker")
    directives.omitted(IAddForm, "date_from")
    date_from = schema.Datetime(
        title=_(u"Query from date"),
        required=False,
    )

    directives.widget("date_to", DatetimeFieldWidget, klass=u"datepicker")
    directives.omitted(IAddForm, "date_to")
    date_to = schema.Datetime(
        title=_(u"Query to date"),
        required=False,
    )

    directives.omitted(IAddForm, "limit")
    limit = schema.Int(
        title=_(u"Limit"),
        description=_(u"Limit Search Results"),
        required=False,
        default=5,
        min=1,
    )

    directives.omitted(IAddForm, "sort_on")
    sort_on = schema.TextLine(
        title=_(u"label_sort_on", default=u"Sort on"),
        description=_(u"Sort the databox on this index"),
        required=False,
    )

    directives.omitted(IAddForm, "sort_reversed")
    sort_reversed = schema.Bool(
        title=_(u"label_sort_reversed", default=u"Reversed order"),
        description=_(u"Sort the results in reversed order"),
        default=False,
        required=False,
    )


@implementer(IDataBoxBehavior)
@adapter(IDexterityContent)
class DataBox(object):

    def __init__(self, context):
        self.context = context
        logger.info("IDataBoxBehavior::__init__:context={}"
                    .format(repr(context)))

    @property
    def query(self):
        """Catalog query
        """
        query = {"portal_type": self.query_type}
        if self.limit:
            query["limit"] = self.limit
        if self.sort_on:
            query["sort_on"] = self.sort_on
        if self.sort_order:
            query["sort_order"] = self.sort_order

        if self.date_index:
            date_from = DateTime(self.date_from or "2000-01-01")
            date_to = DateTime(self.date_to) if self.date_to else DateTime()
            # always make the to_date inclusive
            query[self.date_index] = {
                "query": (date_from, (date_to if date_from <= date_to else date_from) + 1),
                "range": "minmax"
            }

        # update additional queries
        query.update(self.advanced_query)
        logger.info("DataBox Query: {}".format(query))
        return query

    def get_fields(self, portal_type=None):
        """Returns all schema fields of the selected query type

        IMPORTANT: Do not call from within `__init__` due to permissions
        """
        obj = self._create_temporary_object(portal_type=portal_type)
        if obj is None:
            return []
        fields = api.get_fields(obj)
        # drop ignored fields
        for field in IGNORE_FIELDS:
            fields.pop(field, None)
        # Inject Parent Field
        portal_type = api.get_portal_type(obj)
        parent_type = PARENT_TYPES.get(portal_type)
        if parent_type:
            field = ParentField(portal_type=parent_type)
            fields["Parent"] = field
        return fields

    def get_catalog_indexes(self):
        """Returns available catalog indexes for the selected query type
        """
        catalog = api.get_tool(self.get_query_catalog())
        return sorted(catalog.indexes())

    def get_catalog_date_indexes(self):
        """Returns available catalog date indexes for the selected query type
        """
        catalog = api.get_tool(self.get_query_catalog())
        indexes = catalog.getIndexObjects()
        date_indexes = []
        for index in indexes:
            if index.meta_type not in DATE_INDEX_TYPES:
                continue
            name = index.getId()
            date_indexes.append(name)
        return sorted(date_indexes)

    def get_catalog_columns(self):
        """Returns available catalog schema columns for the selected query type
        """
        catalog = api.get_tool(self.get_query_catalog())
        return sorted(catalog.schema())

    @contextmanager
    def temporary_allow_type(self, obj, allowed_type):
        """Temporary allow content type creation in obj
        """
        pt = api.get_tool("portal_types")
        portal_type = obj.portal_type
        fti = pt.get(portal_type)
        # get the current allowed types for the object
        allowed_types = fti.allowed_content_types
        # append the allowed type
        if isinstance(allowed_types, tuple):
            fti.allowed_content_types = allowed_types + (allowed_type, )
        else:
            fti.allowed_content_types = allowed_types + [allowed_type, ]

        yield obj

        # reset the allowed content types
        fti.allowed_content_types = allowed_types

    def _create_temporary_object(self, portal_type=None):
        """Create a temporary object to fetch the fields from

        This is needed to get schema extended fields as well.
        """
        if portal_type is None:
            portal_type = self.query_type
        if portal_type is None:
            return None
        portal_factory = api.get_tool("portal_factory")
        temp_folder = portal_factory._getTempFolder(TMP_FOLDER_KEY)
        if portal_type in temp_folder:
            return temp_folder[portal_type]
        # reduce conflict errors
        portal_factory._p_jar.sync()
        with self.temporary_allow_type(temp_folder, portal_type):
            temp_folder.invokeFactory(portal_type, id=portal_type)
        transaction.commit()
        return temp_folder[portal_type]

    def get_query_catalog(self, default=UID_CATALOG):
        """Returns the primary catalog for the selected query type

        :returns: catalog ID
        """
        catalog = default
        portal_type = self.query_type
        types_tool = api.get_tool("portal_types")
        fti = types_tool.getTypeInfo(portal_type)

        if fti.product:
            # AT content type
            # => Looup via archetype_tool
            archetype_tool = api.get_tool("archetype_tool")
            catalogs = archetype_tool.getCatalogsByType(portal_type)
            catalog_ids = filter(
                lambda cid: cid not in IGNORE_CATALOG_IDS,
                map(lambda cat: cat.getId(), catalogs))
            if len(catalog_ids) > 0:
                catalog = catalog_ids[0]
        else:
            # DX content type
            # => resolve the `_catalogs` attribute from the class
            klass = resolveDottedName(fti.klass)
            # XXX: Refactor multi-catalog behavior to not rely
            #      on this hidden `_catalogs` attribute!
            catalogs = getattr(klass, "_catalogs", [])
            if catalogs:
                catalog = catalogs[0]

        return catalog

    def get_catalog_tool(self):
        """Returns the primary catalog tool for the selected query type
        """
        return api.get_tool(self.get_query_catalog())

    @property
    def sort_order(self):
        if self.sort_reversed is True:
            return "descending"
        return "ascending"

    # Getters and setters for our fields.

    # QUERY TYPE

    def _set_query_type(self, value):
        self.context.query_type = value

    def _get_query_type(self):
        return getattr(self.context, "query_type", None)

    query_type = property(_get_query_type, _set_query_type)

    # COLUMNS

    def _set_columns(self, value):
        self.context.columns = value

    def _get_columns(self):
        columns = getattr(self.context, "columns", []) or []
        # always return by value
        return copy(columns)

    columns = property(_get_columns, _set_columns)

    # ADDITIONAL QUERY

    def _set_advanced_query(self, value):
        if value is None:
            value = {}
        # drop empty items
        value.pop("", None)
        catalog = self.get_catalog_tool()
        for k, v in value.items():
            index = catalog._catalog.getIndex(k)
            meta_type = index.meta_type
            if meta_type in ["BooleanIndex"]:
                v = v in ["True", "1"] and True or False
            elif meta_type in ["DateIndex"]:
                v = parser.parse(v)
            else:
                try:
                    v = ast.literal_eval(v)
                except (ValueError, SyntaxError):
                    pass
            value[k] = v
        self.context.advanced_query = value

    def _get_advanced_query(self):
        query = getattr(self.context, "advanced_query", {}) or {}
        # always return by value
        return copy(query)

    advanced_query = property(_get_advanced_query, _set_advanced_query)

    # DATE INDEX

    def _set_date_index(self, value):
        self.context.date_index = value

    def _get_date_index(self):
        return getattr(self.context, "date_index", None)

    date_index = property(_get_date_index, _set_date_index)

    # DATE FROM

    def _set_date_from(self, value):
        self.context.date_from = value

    def _get_date_from(self):
        value = getattr(self.context, "date_from", None)
        if not isinstance(value, datetime):
            return None
        return value

    date_from = property(_get_date_from, _set_date_from)

    # DATE TO

    def _set_date_to(self, value):
        self.context.date_to = value

    def _get_date_to(self):
        value = getattr(self.context, "date_to", None)
        if not isinstance(value, datetime):
            return None
        return value

    date_to = property(_get_date_to, _set_date_to)

    # LIMIT

    def _set_limit(self, value):
        self.context.limit = value

    def _get_limit(self):
        return getattr(self.context, "limit", 1000)

    limit = property(_get_limit, _set_limit)

    # SORT ON

    def _set_sort_on(self, value):
        self.context.sort_on = value

    def _get_sort_on(self, default="created"):
        return getattr(self.context, "sort_on", default)

    sort_on = property(_get_sort_on, _set_sort_on)

    # SORT REVERSED

    def _set_sort_reversed(self, value):
        self.context.sort_reversed = value

    def _get_sort_reversed(self):
        return getattr(self.context, "sort_reversed", False)

    sort_reversed = property(_get_sort_reversed, _set_sort_reversed)
