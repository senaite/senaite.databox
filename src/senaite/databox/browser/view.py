# -*- coding: utf-8 -*-

import collections

from senaite.core.listing.view import ListingView
from bika.lims import bikaMessageFactory as _


class DataBoxView(ListingView):
    """The default DataBox view
    """
    def __init__(self, context, request):
        super(DataBoxView, self).__init__(context, request)

        self.catalog = "bika_catalog_analysisrequest_listing"
        self.contentFilter = {
            "portal_type": "AnalysisRequest",
            "sort_on": "created",
            "sort_order": "ascending",
        }
        self.pagesize = 10
        self.context_actions = {}
        self.title = self.context.Title()
        self.description = self.context.Description()

        self.columns = collections.OrderedDict((
            ("Title", {
                "title": _("Title"),
                "index": "sortable_title"}),
            ("Description", {
                "title": _("Description"),
                "index": "Description"}),
        ))

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
