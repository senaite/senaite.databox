# -*- coding: utf-8 -*-

import logging

from zope.i18nmessageid import MessageFactory

# Defining a Message Factory for when this product is internationalized.
senaiteMessageFactory = MessageFactory("senaite.databox")

logger = logging.getLogger("senaite.databox")


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    logger.info("*** Initializing SENAITE.DATABOX ***")
