# -*- coding: utf-8 -*-

import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from bika.lims.utils import tmpID
from Products.CMFPlone.utils import _createObjectByType
from senaite.core.listing.view import ListingView
from zope.component import getUtility
from zope.component.interfaces import IFactory


class DataBoxView(ListingView):
    """The default DataBox view
    """
    def __init__(self, context, request):
        super(DataBoxView, self).__init__(context, request)

        self.catalog = self.get_query_catalog()
        self.contentFilter = {
            "portal_type": self.get_query_type(),
            "sort_on": "created",
            "sort_order": "ascending",
        }
        self.pagesize = 10
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

    def create_temporary_object(self):
        """Create a temporary object to fetch the fields from
        """
        types_tool = api.get_tool("portal_types")
        query_type = self.get_query_type()
        fti = types_tool.getTypeInfo(query_type)
        portal_factory = api.get_tool("portal_factory")
        tmp_id = tmpID()

        obj = None

        if fti.product:
            obj = _createObjectByType(query_type, portal_factory, tmp_id)
        else:
            # newstyle factory
            factory = getUtility(IFactory, fti.factory)
            obj = factory(tmp_id)
            if hasattr(obj, '_setPortalTypeName'):
                obj._setPortalTypeName(fti.getId())

        return obj

    def get_query_type(self, default=None):
        """Get the selected query type
        """
        return getattr(self.context, "query_type", default)

    def get_query_catalog(self, default="portal_catalog"):
        """Get the ID of the catalog to query
        """
        archetype_tool = api.get_tool("archetype_tool")
        query_type = self.get_query_type()
        catalogs = archetype_tool.getCatalogsByType(query_type)
        if len(catalogs) == 0:
            return default
        primary_catalog = catalogs[0]
        return primary_catalog.getId()

    def get_columns(self):
        """
        """
        columns = collections.OrderedDict((
            ("Title", {
                "title": _("Title"),
                "index": "sortable_title"}),
            ("Description", {
                "title": _("Description"),
                "index": "Description"}),
        ))

        return columns
