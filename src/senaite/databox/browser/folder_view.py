# -*- coding: utf-8 -*-

import collections

from bika.lims import api
from bika.lims import senaiteMessageFactory as _
from bika.lims.utils import get_link
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
            "sort_order": "descending",
        }

        self.context_actions = {
            _("Add"): {
                "url": "++add++DataBox",
                "permission": "cmf.AddPortalContent",
                "icon": "++resource++bika.lims.images/add.png"}
            }

        self.icon = "{}/{}".format(
            self.portal_url, "senaite_theme/icon/databoxfolder")

        self.title = self.context.Title()
        self.description = self.context.Description()
        self.show_select_column = False
        self.pagesize = 25

        self.columns = collections.OrderedDict((
            ("Title", {
                "title": _("Title"),
                "index": "sortable_title"}),
            ("Description", {
                "title": _("Description"),
                "index": "Description"}),
            ("query_type", {
                "title": _("Type"),
                "index": "query_type"}),
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

    def folderitem(self, obj, item, index):
        obj = api.get_object(obj)
        url = api.get_url(obj)
        title = api.get_title(obj)
        item["replace"]["Title"] = get_link(
            url, value=title)
        item["query_type"] = getattr(obj, "query_type", None)
        return item
