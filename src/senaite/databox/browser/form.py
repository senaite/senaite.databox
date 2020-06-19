# -*- coding: utf-8 -*-

from bika.lims import api
from bika.lims.browser import BrowserView
from dateutil import parser
from plone.protect import PostOnly
from plone.protect import protect
from senaite.databox import logger
from senaite.databox.behaviors.databox import IDataBoxBehavior


class FormController(BrowserView):
    """DataBox Form Controller View
    """

    def __init__(self, context, request):
        super(FormController, self).__init__(context, request)

        self.context = context
        self.request = request
        self.hash = request.form.get("hash", "#query")
        self.exit_url = "{}{}".format(
            api.get_url(context), self.hash)
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
            value = parser.parse(value)
        # TODO: Review the data structure to avoid processing
        if key == "columns":
            columns = []
            for record in value:
                record = dict(record)
                column = record.pop("column")
                columns.append({column: record})
            return columns
        return value
