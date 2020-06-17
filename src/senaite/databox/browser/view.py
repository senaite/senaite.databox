# -*- coding: utf-8 -*-

import collections
import json

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from plone.memoize import view
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from senaite.core.listing.view import ListingView
from senaite.core.supermodel.model import SuperModel
from senaite.databox.behaviors.databox import IDataBoxBehavior
from senaite.databox.interfaces import IFieldConverter
from zope.component import getUtilitiesFor
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import alsoProvides
from zope.schema.interfaces import IVocabularyFactory

REFERENCE_FIELD_TYPES = [
    "reference",
]
DEFAULT_REF_FIELD = "title"


class DataBoxView(ListingView):
    """The default DataBox view
    """
    template = ViewPageTemplateFile("templates/databox_view.pt")
    controls = ViewPageTemplateFile("templates/databox_controls.pt")

    def __init__(self, context, request):
        super(DataBoxView, self).__init__(context, request)

        self.contentFilter = self.databox.query

        self.pagesize = self.databox.limit
        self.context_actions = {}
        self.title = self.context.Title()
        self.description = self.context.Description()

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
        """Update hook
        """
        super(DataBoxView, self).update()

    def before_render(self):
        """Before template render hook
        """
        super(DataBoxView, self).before_render()

    @view.memoize
    def settings(self):
        return {
            "data-databox_id":  api.get_id(self.context),
            "data-databox_uid": api.get_uid(self.context),
            "data-query_type": self.context.query_type,
            "data-sort_on":  json.dumps(self.context.sort_on),
            "data-sort_reversed": json.dumps(self.databox.sort_order),
            "data-query_types": json.dumps(self.get_query_types()),
        }

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
        return self.databox.get_catalog_indexes()

    @view.memoize
    def get_catalog_date_indexes(self):
        return self.databox.get_catalog_date_indexes()

    @view.memoize
    def get_schema_fields(self):
        # NOTE: we disable CSRF protection because the databox creates a
        # temporary object to fetch the form fields (write on read)
        alsoProvides(self.request, IDisableCSRFProtection)
        fields = self.databox.get_fields()
        return sorted(fields.keys())

    def get_columns(self):
        """Calculate visible columns
        """
        columns = self.databox.get_column_config()
        if columns:
            return columns

        # default columns
        columns = collections.OrderedDict((
            ("title", {
                "title": _("Title")
            }),
            ("description", {
                "title": _("Description"),
            }),
        ))
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

    def get_refs_for(self, column):
        """Dereference field references
        """
        out = []
        config = self.columns[column]
        refs = config.get("refs")
        if refs is None:
            return []
        # check if the column is a valid type
        pt = api.get_tool("portal_types")
        if column not in pt.listContentTypes():
            return []

        # column is a reference field to another object
        for num, ref in enumerate(refs):
            fields = self.databox.get_fields(portal_type=column)
            out.append({
                "key": ref,
                "fields": sorted(fields.keys()),
            })
            # check if the last field is a reference
            if num + 1 == len(refs):
                field = fields.get(ref)
                if field.type in REFERENCE_FIELD_TYPES:
                    out.append({
                        "key": DEFAULT_REF_FIELD,
                        "fields": sorted(fields.keys()),
                    })
        return out

    def dereference_model_item(self, model, refs):
        """Recursively dereferences model attributes
        """
        value = model.get(DEFAULT_REF_FIELD)
        for ref in refs:
            value = model.get(ref)
            if isinstance(value, SuperModel):
                return self.dereference_model_item(value, refs[1:])
        return value

    def folderitem(self, obj, item, index):
        model = SuperModel(obj)
        for column, config in self.columns.items():
            value = model.get(column)
            converter = config.get("converter")
            if isinstance(value, SuperModel):
                refs = config.get("refs", ["title"])
                value = self.dereference_model_item(value, refs)
                config["refs"] = refs
            if converter:
                func = queryUtility(IFieldConverter, name=converter)
                if callable(func):
                    value = func(obj, column, value)
            item[column] = value
        return item
