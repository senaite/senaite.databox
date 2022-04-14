# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.databox import logger

PROFILE_ID = "profile-senaite.databox:default"


def run_all_upgradesteps(portal_setup):
    """Run all upgrade steps

    :param portal_setup: The portal_setup tool
    """

    logger.info("Run upgrade steps for SENAITE DATABOX ...")
    context = portal_setup._getImportContext(PROFILE_ID)
    portal = context.getSite()
    portal_setup.runAllImportStepsFromProfile(PROFILE_ID)
    update_security_settings(portal)
    logger.info("Run upgrade steps for SENAITE DATABOX [DONE]")


def update_security_settings(portal):
    """Update security settings for Databoxes
    """
    logger.info("Updating security settings for databoxes ...")
    databoxes = portal.get("databoxes")
    for databox in databoxes.objectValues():
        update_rolemappings_for(databox)
    update_rolemappings_for(databoxes)
    databoxes.reindexObject()
    logger.info("Updating security settings for databoxes [DONE]")


def update_rolemappings_for(context):
    """update rolemappings
    """
    wf_tool = api.get_tool("portal_workflow")
    wf_ids = wf_tool.getChainFor(context)
    for wf_id in wf_ids:
        wf = wf_tool.getWorkflowById(wf_id)
        if wf is not None:
            wf.updateRoleMappingsFor(context)
            message = "Updated rolemappings for {}".format(repr(context))
            logger.info(message)
