# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.DATABOX
#
# Copyright 2018 by it's authors.

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from senaite import api
from senaite.core.supermodel import SuperModel

# from plone.dexterity.browser import add
# from plone.dexterity.browser.view import DefaultView

from senaite.databox import logger


class DataBoxFolderView(BrowserView):
    """
    """
    template = ViewPageTemplateFile("templates/databox_folder_view.pt")

    def __init__(self, context, request):
        logger.info("DataBoxFolderView::init")
        super(DataBoxFolderView, self).__init__(context, request)
        self.context = context
        self.request = request

    def __call__(self):
        logger.info("DataBoxFolderView::call")
        return self.template()


class DataBoxView(BrowserView):
    """The default DataBox view
    """
    template = ViewPageTemplateFile("templates/databox_view.pt")

    def __init__(self, context, request):
        super(DataBoxView, self).__init__(context, request)
        self.context = context
        self.request = request

    def __call__(self):
        return self.template()

    @property
    def portal_type(self):
        """Each databox need a unique portal_type
        """
        return "AnalysisRequest"

    @property
    def query(self):
        """The catalog query to execute

        The query must be stored on the databox as configuration.
        The UI need to provide similar fields like a collection, but with the
        capability to chose the right catalog for a preview.
        """
        return {
            "portal_type": self.portal_type
        }

    def get_catalog(self, portal_type=None):
        """Returns the primary catalog of the queried portal type
        """
        portal_catalog = api.get_tool("portal_catalog")
        if portal_type is None:
            logger.warn("No portal_type given, returning portal_catalog")
            return portal_catalog
        at_tool = api.get_tool("archetype_tool")
        catalogs = at_tool.getCatalogsByType(portal_type)
        if not catalogs:
            return portal_catalog
        return catalogs[0]

    def columns(self):
        """The configured columns.

        The columns need to get stored on the databox as configuration.
        The UI need to provide these columns as select options through a
        lookup of the selected portal_type.
        """
        return [
            "title",
            "id",
            "SampleTypeTitle",
        ]

    def collection(self):
        portal_type = self.portal_type
        catalog = self.get_catalog(portal_type)
        results = catalog(self.query)
        return map(lambda brain: SuperModel(brain.UID), results)


class DataBoxEdit(BrowserView):
    """Custom DataBox Edit View

    Probably best to do a plain browser view and all the magic in JS?
    """
    template = ViewPageTemplateFile("templates/databox_edit.pt")

    def __init__(self, context, request):
        logger.info("DataBoxEdit::init")
        super(DataBoxEdit, self).__init__(context, request)
        self.context = context
        self.request = request

    def __call__(self):
        logger.info("DataBoxEdit::call")
        return self.template()
