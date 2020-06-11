# -*- coding: utf-8 -*-

import collections

from bika.lims import bikaMessageFactory as _
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
        self.adapted = adapted = IDataBoxBehavior(context)

        self.catalog = adapted.get_query_catalog()
        sort_order = "descending" if adapted.sort_reversed else "ascending"
        self.contentFilter = {
            "portal_type": adapted.query_type,
            "sort_on": adapted.sort_on,
            "sort_order": sort_order
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

    @set_application_json_header
    @returns_safe_json
    def ajax_query_types(self):
        """Returns the `query_types` list of the context as JSON
        """
        factory = getUtility(
            IVocabularyFactory, "senaite.databox.vocabularies.query_types")
        vocabulary = factory(self.context)
        return sorted(vocabulary.by_value.keys())
