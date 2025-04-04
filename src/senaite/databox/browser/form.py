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

from bika.lims import api
from bika.lims.browser import BrowserView
from dateutil import parser
from plone.protect import PostOnly
from plone.protect import protect
from senaite.databox import logger
from senaite.databox.behaviors.databox import IDataBoxBehavior
from zope.lifecycleevent import modified


class FormController(BrowserView):
    """DataBox Form Controller View
    """

    def __init__(self, context, request):
        super(FormController, self).__init__(context, request)

        self.context = context
        self.request = request
        self.tab = request.form.get("tab", "query")
        self.exit_url = "{}?tab={}".format(
            api.get_url(context), self.tab)
        self.prefix = "senaite.databox"

    def __call__(self):
        if self.request.form.get("submitted", False):
            self.handle_submit(REQUEST=self.request)
        return self.request.response.redirect(self.exit_url)

    @property
    def databox(self):
        """Returns the adapted databox context
        """
        return IDataBoxBehavior(self.context)

    @protect(PostOnly)
    def handle_submit(self, REQUEST=None):
        logger.info("senaite.databox::handle_submit")
        form_data = self.get_form_data()
        for key, value in form_data.items():
            logger.info("Set field '{}' -> {}".format(key, value))
            setattr(self.databox, key, value)
        modified(self.context)

    def get_form_data(self):
        """Returns the processed form data
        """
        data = {}
        for key, value in self.request.form.items():
            # skipping non-prefixed keys
            if not key.startswith(self.prefix):
                continue
            key = key.split(".")[-1]
            value = self._process_form_value(key, value)
            data[key] = value
        return data

    def _process_form_value(self, key, value):
        """Process the form value for the databox
        """
        if key in ["date_from", "date_to"]:
            if value:
                return parser.parse(value)

        # TODO: Review the data structure to avoid processing
        if key == "columns":
            columns = []
            for record in value:
                record = dict(record)
                columns.append({record["column"]: record})
            return columns

        if key == "advanced_query":
            query = {}
            for record in value:
                if record.get("delete"):
                    continue
                query[record.get("index")] = record.get("value")
            return query

        return value
