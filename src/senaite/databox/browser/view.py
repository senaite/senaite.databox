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

import collections
import csv
import StringIO
import sys

import six

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from DateTime import DateTime
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from plone.memoize import view
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from senaite.app.listing.view import ListingView
from senaite.app.supermodel.model import SuperModel
from senaite.core.api import dtime
from senaite.databox import logger
from senaite.databox.behaviors.databox import IDataBoxBehavior
from senaite.databox.interfaces import IFieldConverter
from senaite.databox.permissions import ManageDataBox
from z3c.form.interfaces import DISPLAY_MODE
from z3c.form.interfaces import IDataConverter
from z3c.form.interfaces import IFieldWidget
from zope.component import getMultiAdapter
from zope.component import getUtilitiesFor
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import alsoProvides
from zope.schema.interfaces import IField
from zope.schema.interfaces import IVocabularyFactory

DEFAULT_REF = "title"
REF_FIELD_TYPES = ["reference", "uidreference"]


class DataBoxView(ListingView):
    """The default DataBox view
    """
    template = ViewPageTemplateFile("templates/databox_view.pt")

    def __init__(self, context, request):
        super(DataBoxView, self).__init__(context, request)

        self.contentFilter = self.databox.query

        self.pagesize = self.databox.limit
        self.context_actions = {}
        self.title = self.context.Title()
        self.description = self.context.Description()
        self.show_select_column = True

        self.columns = self.get_columns()

        self.review_states = [
            {
                "id": "default",
                "title": _("All"),
                "contentFilter": {},
                "transitions": [],
                "custom_transitions": [],
                "columns": self.columns.keys()
            }
        ]

    def update(self):
        super(DataBoxView, self).update()

    def render_databox_controls(self):
        """Renders the databox controls edit form
        """
        # N.B.: the form controls implicitly create a temporary object to fetch
        #       the available (and extended) schema fields.
        if not api.security.check_permission(ManageDataBox, self.context):
            return ""
        return ViewPageTemplateFile("templates/databox_controls.pt")(self)

    def widgets(self, mode=DISPLAY_MODE):
        """Return the widgets for the databox

        # https://stackoverflow.com/questions/8476781/how-to-access-z3c-form-widget-settings-from-browser-view
        """
        widgets = []
        fields = api.get_fields(self.context)
        for name, field in fields.items():
            widget = getMultiAdapter((field, self.request), IFieldWidget)
            widget.mode = mode
            widget.context = self.context
            converter = IDataConverter(widget)
            value = field.get(self.context)
            widget.value = converter.toWidgetValue(value)
            widget.update()
            widgets.append(widget)
        return widgets

    def export_to_csv(self):
        """Action handler export to CSV
        """
        self.pagesize = sys.maxint
        filename = "{}.csv".format(self.context.Title())
        data = self.get_csv()
        return self.download(data, filename)

    def export_to_excel(self):
        """Action handler export to Excel
        """
        self.pagesize = sys.maxint
        filename = "{}.xlsx".format(self.context.Title())
        data = self.get_excel()
        return self.download(data, filename, type="application/vnd.ms-excel")

    def get_rows(self, header=True):
        """Extract the rows from the folderitems
        """
        if header:
            yield map(lambda v: v.get("title"), self.columns.values())
        keys = self.columns.keys()
        for item in self.folderitems():
            yield map(lambda key: self.to_string(item.get(key)), keys)

    def to_string(self, value):
        """Convert value to string
        """
        if isinstance(value, six.string_types):
            return value
        elif isinstance(value, DateTime):
            return value.ISO()
        return str(value)

    def get_csv(self, delimiter=",", quotechar='"',
                quoting=csv.QUOTE_ALL, dialect=csv.excel):
        """Export databox to CSV
        """
        csvfile = StringIO.StringIO()
        writer = csv.writer(csvfile,
                            delimiter=delimiter,
                            quotechar=quotechar,
                            quoting=quoting,
                            dialect=dialect)

        # write the rows as CSV
        for row in self.get_rows():
            def to_utf8(s):
                return api.safe_unicode(s).encode("utf8")
            writer.writerow(map(to_utf8, row))

        return csvfile.getvalue()

    def get_excel(self):
        """Export databox to Excel
        """
        workbook = Workbook()
        first_sheet = workbook.get_active_sheet()
        first_sheet.title = api.safe_unicode(self.context.Title())
        for row in self.get_rows():
            first_sheet.append(row)
        return save_virtual_workbook(workbook)

    def download(self, data, filename, type="text/csv"):
        response = self.request.response
        response.setHeader("Content-Disposition",
                           "attachment; filename={}".format(filename))
        response.setHeader("Content-Type", "{}; charset=utf-8".format(type))
        response.setHeader("Content-Length", len(data))
        response.setHeader("Cache-Control", "no-store")
        response.setHeader("Pragma", "no-cache")
        response.write(data)

    @property
    @view.memoize
    def databox(self):
        """Returns the adapted databox context
        """
        return IDataBoxBehavior(self.context)

    @property
    @view.memoize
    def catalog(self):
        return self.databox.get_query_catalog()

    @property
    def date_from(self):
        if not self.context.date_from:
            return ""
        return dtime.date_to_string(self.context.date_from)

    @property
    def date_to(self):
        if not self.context.date_to:
            return ""
        if self.context.date_from and self.context.date_to < self.context.date_from:
            return dtime.date_to_string(self.context.date_from)
        return dtime.date_to_string(self.context.date_to)

    @view.memoize
    def get_query_types(self):
        """Returns the `query_types` list of the context as JSON
        """
        factory = getUtility(
            IVocabularyFactory, "senaite.databox.vocabularies.query_types")
        vocabulary = factory(self.context)
        return sorted(vocabulary.by_value.keys())

    @view.memoize
    def get_catalog_indexes(self):
        indexes = self.databox.get_catalog_indexes()
        # insert an empty item
        indexes.insert(0, "")
        return indexes

    @view.memoize
    def get_catalog_sort_indexes(self):
        indexes = []
        catalog = self.databox.get_catalog_tool()
        for key in catalog.indexes():
            index = catalog.Indexes.get(key)
            if not hasattr(index, "documentToKeyMap"):
                continue
            indexes.append(key)
        # insert an empty item
        indexes.insert(0, "")
        return indexes

    @view.memoize
    def get_catalog_date_indexes(self):
        indexes = self.databox.get_catalog_date_indexes()
        # insert an empty item
        indexes.insert(0, "")
        return indexes

    @view.memoize
    def get_advanced_query(self):
        advanced_query = self.databox.advanced_query
        # insert an empty item
        advanced_query.update({"": ""})
        return advanced_query

    @view.memoize
    def get_schema_fields(self):
        # NOTE: we disable CSRF protection because the databox creates a
        # temporary object to fetch the form fields (write on read)
        alsoProvides(self.request, IDisableCSRFProtection)
        fields = self.databox.get_fields().keys()
        # fields.extend(self.databox.get_catalog_columns())
        return sorted(fields)

    def get_columns(self):
        """Calculate visible columns
        """
        columns = collections.OrderedDict()

        if not self.databox.columns:
            # default columns
            columns["0"] = {"column": "title", "title": _("Title")}

        for num, record in enumerate(self.databox.columns):
            key, column = record.items()[0]
            # databox columns are not sortable by the catalog, even not manual,
            # because the real values are dereferenced in `folderitem`.
            column["sortable"] = False
            columns[str(num)] = column

        return columns

    def get_converters(self):
        """Get all available converter utilities
        """
        converters = [{"name": "", "description": ""}]
        utilities = getUtilitiesFor(IFieldConverter)
        for utility in utilities:
            name, component = utility
            converters.append({
                "name": name,
                "description": component.__doc__,
            })
        return converters

    def get_type_info(self, portal_type):
        """Returns the portal type information for the given type

        :returns: FTI or None
        """
        pt = api.get_tool("portal_types")
        return pt.getTypeInfo(portal_type)

    def is_reference_field(self, field):
        """Checks if the field is a reference field type
        """
        if not field:
            return False
        if IField.providedBy(field):
            # TODO: At the moment we do not have a dexterity based reference
            #       field. Implement this when we have an interface for this.
            return False
        field_type = getattr(field, "type", None)
        if field_type is None:
            return False
        return field.type in REF_FIELD_TYPES

    def get_reftype(self, field):
        """Returns the first allowed type of the reference field
        """
        portal_type = getattr(field, "portal_type", None)
        if portal_type:
            return portal_type
        allowed_types = getattr(field, "allowed_types", [])
        if not allowed_types:
            return None
        if not isinstance(allowed_types, (list, tuple)):
            return allowed_types
        return allowed_types[0]

    def get_reference_columns(self, column):
        """Returns configured reference columns for the given colum

        Called from the page template to render the column controls.

        Note: Here we need to work without any real objects!
              This is just to configure the column config for the query
        """

        columns = []

        # get the column data from the columns config
        column_data = self.columns.get(column)

        # get the column key
        column_key = column_data.get("column")

        # get all fields of the databox
        fields = self.databox.get_fields()

        # get the requested field
        field = fields.get(column_key)

        # return immediately if the field is not a reference field
        if not self.is_reference_field(field):
            return columns

        # check if we have further stored references
        refs = column_data.get("refs", [DEFAULT_REF])

        logger.info("Reference Columns '{}' -> {}".format(column, refs))

        # get the fields of the referenced object
        ref_type = self.get_reftype(field)
        ref_fields = self.databox.get_fields(portal_type=ref_type)

        for num, ref in enumerate(refs):

            # get the field of the referenced object
            field = ref_fields.get(ref)

            if field is None:
                continue

            columns.append({
                "key": ref,
                "type": ref_type,
                "fields": sorted(ref_fields),
            })

            # get the fields of the referenced object
            ref_type = self.get_reftype(field)
            ref_fields = self.databox.get_fields(portal_type=ref_type)

            # not a reference anymore, break
            if not ref_type:
                break

            if num == len(refs) - 1:
                if self.is_reference_field(field):
                    ref_type = self.get_reftype(field)
                    ref_fields = self.databox.get_fields(portal_type=ref_type)
                    columns.append({
                        "key": DEFAULT_REF,
                        "type": ref_type,
                        "fields": sorted(ref_fields),
                    })

        return columns

    def resolve_reference_model(self, model, refs=None):
        """Dereferences a list of attributes of a given model

        :param model: SuperModel to be traversed
        :param refs: List of attributes to traverse
        :returns: Dereferenced model
        """
        if not isinstance(refs, list):
            return model
        for ref in refs:
            value = model.get(ref)
            if isinstance(value, SuperModel):
                model = self.resolve_reference_model(value, refs[1:])
        return model

    def execute_code(self, code, **kw):
        """Executed the code
        """
        kw.update({
            "api": api,
        })
        try:
            return eval(code, kw)
        except Exception as exc:
            return repr(exc)

    def folderitem(self, obj, item, index):
        """Applies new properties to the item being rendered in the list

        :param obj: object to be rendered as a row in the list
        :param item: dict representation of the obj suitable for the listing
        :param index: current index within the list of items
        :type obj: CatalogBrain
        :type item: dict
        :type index: int
        :return: the dict representation of the item
        :rtype: dict
        """
        brain = obj
        obj = api.get_object(obj)

        for column, config in self.columns.items():
            key = config.get("column")

            model = SuperModel(obj)
            if key == "Parent":
                value = SuperModel(api.get_parent(obj))
            elif key == "Result" and getattr(obj, "getFormattedResult", None):
                value = obj.getFormattedResult()
            else:
                value = model.get(key)

            # Handle reference columns
            if isinstance(value, SuperModel):
                # reference columns are stored in the column config
                refs = config.get("refs", [DEFAULT_REF])
                # resolve the referenced model
                model = self.resolve_reference_model(value, refs)
                # get the last selected reference column
                ref = refs[-1]
                # get the referenced value
                value = model.get(ref)

            if callable(value):
                value = value()

            code = config.get("code")
            if code:
                # use the referenced instance as the context
                context = model.instance
                # execute the code
                value = self.execute_code(
                    code, obj=obj, context=context, model=model, brain=brain)

            converter = config.get("converter")
            if converter:
                func = queryUtility(IFieldConverter, name=converter)
                if callable(func):
                    converted_value = func(model.instance, column, value)
                    item["replace"][column] = converted_value

            item[column] = value
        return item
