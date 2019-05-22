# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.DATABOX
#
# Copyright 2018 by it's authors.

import inspect

from plone.dexterity.browser import edit
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from senaite import api
from senaite.core.supermodel import SuperModel
from senaite.databox import logger
from senaite.databox.decorators import returns_json
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from plone.app.layout.globals.interfaces import IViewView


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
    implements(IViewView, IPublishTraverse)

    template = ViewPageTemplateFile("templates/databox_view.pt")

    def __init__(self, context, request):
        super(DataBoxView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.traverse_subpath = []

    def __call__(self):
        if len(self.traverse_subpath) < 1:
            return self.template()

        # check if the method exists
        func_arg = self.traverse_subpath[0]
        func_name = "ajax_{}".format(func_arg)

        func = getattr(self, func_name, None)
        if func is None:
            return self.fail("Invalid function", status=400)

        # Additional provided path segments after the function name are handled
        # as positional arguments
        args = self.traverse_subpath[1:]

        # check mandatory arguments
        func_sig = inspect.getargspec(func)
        # positional arguments after `self` argument
        required_args = func_sig.args[1:]

        if len(args) < len(required_args):
            return self.fail("Wrong signature, please use '{}/{}'"
                             .format(func_arg, "/".join(required_args)), 400)
        return func(*args)

    def publishTraverse(self, request, name):
        """Called before __call__ for each path name
        """
        self.traverse_subpath.append(name)
        return self

    @property
    def keys(self):
        """Return the colum keys
        """
        return map(lambda item: self.translate(item[0]), self.columns)

    @property
    def values(self):
        """Return the column values
        """
        return map(lambda item: item[1], self.columns)

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

        TODO: We need also provide a converter function to process e.g. date
              values or other fields that need conversion of their raw value
        """
        return [
            ("Title", "Title"),
            ("Description", "Description"),
            ("Sample Type", "SampleTypeTitle"),
            ("Contact", "Contact.Fullname"),
            ("Date Received", "DateReceived"),
            ("Date Sampled", "DateSampled"),
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

    def get(self, obj, key, default=None):
        """Get a context value by key
        """
        v = obj
        for k in key.split("."):
            if v is None:
                logger.warn("No reference found for key={} on object={}"
                            .format(key, obj.id))
                return default
            v = v.get(k)
        if callable(v):
            v = v()
        return v

    def pick(self, model, *keys):
        """Returns a dictionary filtered to only have model values for the
           whitelisted keys (or list of valid keys)

        >>> data = pick(model, "absolute_url", "UID")
        >>> len(data) == 2
        True
        >>> data["absolute_url"] == model.absolute_url()
        True
        >>> data["UID"] == model.UID()
        True
        """
        data = dict()
        marker = object()

        for key in keys:
            value = self.get(model, key, marker)
            if value is not marker:
                data[key] = model.stringify(value)
        return data

    @returns_json
    def ajax_to_json(self):
        """Extracts the JSON from the request
        """
        return map(lambda m: self.pick(m, *self.values),
                   self.collection)


class DataBoxEdit(edit.DefaultEditForm):
    """Custom DataBox Edit View

    Probably best to do a plain browser view and all the magic in JS?
    """
    template = ViewPageTemplateFile("templates/databox_edit.pt")

    # def __init__(self, context, request):
    #     logger.info("DataBoxEdit::init")
    #     super(DataBoxEdit, self).__init__(context, request)
    #     self.context = context
    #     self.request = request

    # def __call__(self):
    #     logger.info("DataBoxEdit::call")
    #     return self.template()
