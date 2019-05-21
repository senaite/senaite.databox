# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.DATABOX
#
# Copyright 2018 by it's authors.

from plone.dexterity.browser import add


class AddForm(add.DefaultAddForm):
    portal_type = "DataBox"


class AddView(add.DefaultAddView):
    form = AddForm

    def __init__(self, context, request, ti=None):
        super(AddView, self).__init__(context, request, ti=ti)
