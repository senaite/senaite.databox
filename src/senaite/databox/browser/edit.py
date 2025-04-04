# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.DATABOX.
#
# SENAITE.DATABOX is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2018-2025 by it's authors.
# Some rights reserved, see README and LICENSE.

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

    def update(self):
        """super class updateWidgets

        self.widgets.keys()
        ['IBasic.title', 'IBasic.description', 'query_type']
        """
        super(DataBoxEdit, self).update()
