# -*- coding: utf-8 -*-

from plone.dexterity.browser import edit
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from senaite.databox import logger


class DataBoxEdit(edit.DefaultEditForm):
    """Custom DataBox Edit View

    NOTE: This is a ReactJS controlled component
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
