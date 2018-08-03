# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.DATABOX
#
# Copyright 2018 by it's authors.

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from senaite import api
from senaite.core.supermodel import SuperModel
from senaite.databox import logger
from Products.CMFPlone.utils import safe_unicode
from plone.dexterity.browser import edit


class DataBoxFolderView(BrowserView):
    """The DataBox Folder View
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
    def header(self):
        """Return the colum header titles
        """
        return map(lambda item: self.translate(item[0]), self.columns)

    @property
    def portal_type(self):
        """Each databox need a unique portal_type
        """
        return self.context.content_type

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

    @property
    def columns(self):
        """The configured columns.

        The columns need to get stored on the databox as configuration.
        The UI need to provide these columns as select options through a
        lookup of the selected portal_type.
        """
        return [
            ("Title", "title"),
            ("Description", "Description"),
            ("Sample Type", "Sample.SampleType.Title"),
        ]

    @property
    def collection(self):
        """The collection of result models
        """
        catalog = self.get_catalog()
        results = catalog(self.query)
        models = map(lambda brain: SuperModel(brain.UID), results)
        return models

    def translate(self, value):
        value = safe_unicode(value)
        value = self.context.translate(value, domain="senaite.core")
        return value

    def get_catalog(self):
        """Returns the primary catalog of the queried portal type
        """
        portal_catalog = api.get_tool("portal_catalog")
        at_tool = api.get_tool("archetype_tool")
        catalogs = at_tool.getCatalogsByType(self.portal_type)
        if not catalogs:
            return portal_catalog
        return catalogs[0]

    def get(self, obj, key):
        """Get a context value by key
        """
        v = obj
        for k in key.split("."):
            if v is None:
                logger.warn("No reference found for key={} on object={}"
                            .format(key, obj.id))
                break
            v = v.get(k)
        if callable(v):
            v = v()
        return v


class DataBoxEdit(edit.DefaultEditForm):
    """Custom DataBox Edit View

    Probably best to do a plain browser view and all the magic in JS?
    """
    # template = ViewPageTemplateFile("templates/databox_edit.pt")

    # def __init__(self, context, request):
    #     logger.info("DataBoxEdit::init")
    #     super(DataBoxEdit, self).__init__(context, request)
    #     self.context = context
    #     self.request = request

    # def __call__(self):
    #     logger.info("DataBoxEdit::call")
    #     return self.template()
