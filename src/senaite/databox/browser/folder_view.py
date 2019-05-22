# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from senaite.databox import logger


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
