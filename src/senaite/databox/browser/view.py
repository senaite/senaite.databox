# -*- coding: utf-8 -*-

import collections

from bika.lims import bikaMessageFactory as _
from senaite.core.listing.view import ListingView
from senaite.core.supermodel.model import SuperModel
from senaite.databox.behaviors.databox import IDataBoxBehavior


class DataBoxView(ListingView):
    """The default DataBox view
    """
    def __init__(self, context, request):
        super(DataBoxView, self).__init__(context, request)
        adapted = IDataBoxBehavior(context)

        self.catalog = adapted.get_query_catalog()
        self.contentFilter = {
            "portal_type": adapted.query_type,
            "sort_on": adapted.sort_on,
            "sort_order": "ascending",
        }
        self.pagesize = adapted.limit
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

    def get_columns(self):
        """
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
