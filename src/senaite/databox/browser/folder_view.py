# -*- coding: utf-8 -*-

import collections

from bika.lims import bikaMessageFactory as _
from senaite.core.listing.view import ListingView


class DataBoxFolderView(ListingView):
    """The DataBox Folder View
    """

    def __init__(self, context, request):
        super(DataBoxFolderView, self).__init__(context, request)

        self.catalog = "portal_catalog"

        self.contentFilter = {
            "portal_type": "DataBox",
            "sort_on": "created",
            "sort_order": "ascending",
        }

        self.context_actions = {
            _("Add"): {
                "url": "++add++DataBox",
                "permission": "cmf.AddPortalContent",
                "icon": "++resource++bika.lims.images/add.png"}
            }

        self.icon = "{}/{}/{}".format(
            self.portal_url,
            "/++resource++senaite.databox.static",
            "images/databoxfolder_icon_64x64.png"
        )

        self.title = self.context.Title()
        self.description = self.context.Description()
        self.show_select_column = True
        self.pagesize = 25

        self.columns = collections.OrderedDict((
            ("Title", {
                "title": _("Title"),
                "replace_url": "absolute_url",
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
        super(DataBoxFolderView, self).update()

    def before_render(self):
        """Before template render hook
        """
        super(DataBoxFolderView, self).before_render()
        # Don't allow any context actions
        self.request.set("disable_border", 1)
