# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.DATABOX
#
# Copyright 2018 by it's authors.

from bika.lims.idserver import renameAfterCreation
from senaite.databox import logger


def auto_generate_id(obj, event):
    """Generate ID with the IDServer from senaite.core
    """
    logger.info("Auto-Generate ID for {}".format(repr(obj)))
    renameAfterCreation(obj)
