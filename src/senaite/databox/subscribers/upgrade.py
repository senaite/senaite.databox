# -*- coding: utf-8 -*-

from bika.lims.api import get_portal
from senaite.databox import is_installed
from senaite.databox.setuphandlers import setup_navigation_types
from senaite.databox import logger


def afterUpgradeStepHandler(event):
    """Event handler that is executed after running an upgrade step of senaite.core
    """
    if not is_installed():
        return
    logger.info("Run senaite.databox.afterUpgradeStepHandler ...")
    portal = get_portal()
    setup_navigation_types(portal)
    logger.info("Run senaite.databox.afterUpgradeStepHandler [DONE]")
