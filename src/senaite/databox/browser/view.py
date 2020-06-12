# -*- coding: utf-8 -*-

import json
import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from plone.memoize import view
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from senaite.core.listing.decorators import returns_safe_json
from senaite.core.listing.decorators import set_application_json_header
from senaite.core.listing.view import ListingView
from senaite.core.supermodel.model import SuperModel
from senaite.databox.behaviors.databox import IDataBoxBehavior
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class DataBoxView(ListingView):
    """The default DataBox view
    """
    template = ViewPageTemplateFile("templates/databox_view.pt")

    def __init__(self, context, request):
        super(DataBoxView, self).__init__(context, request)

        self.contentFilter = {
            "portal_type": self.context.query_type,
            "sort_on": self.context.sort_on,
            "sort_order": self.databox.sort_order
        }
        self.pagesize = self.context.limit
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

    def get_columns(self):
        """Calculate visible columns
        """
        adapted = IDataBoxBehavior(self.context)
        columns = collections.OrderedDict()

        for column in adapted.display_columns:
            columns[column] = {
                "title": column
            }
        return columns

    def folderitem(self, obj, item, index):
        model = SuperModel(obj)
        for column in self.columns:
            value = model.get(column)
            if isinstance(value, SuperModel):
                value = value.get("title")
            item[column] = value
        return item

