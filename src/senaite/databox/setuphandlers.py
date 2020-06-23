# -*- coding: utf-8 -*-

from senaite.databox import logger
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

DATABOX_TYPES = [
    "DataBox",
    "DataBoxFolder",
]


def setup_handler(context):
    """Generic setup handler
    """

    if context.readDataFile("senaite.databox.txt") is None:
        return

    logger.info("SENAITE.DATABOX setup handler [BEGIN]")
    portal = context.getSite()  # noqa
    add_databoxes_folder(portal)
    setup_navigation_types(portal)
    logger.info("SENAITE.DATABOX setup handler [DONE]")


def add_databoxes_folder(portal):
    """Adds the initial Databox folder
    """
    if portal.get("databoxes") is None:
        logger.info("Adding DataBox Folder")
        portal.invokeFactory("DataBoxFolder", "databoxes", title="Databoxes")


def setup_navigation_types(portal):
    """Add additional types for navigation
    """
    registry = getUtility(IRegistry)
    key = "plone.displayed_types"
    display_types = registry.get(key, ())

    new_display_types = set(display_types)
    new_display_types.update(DATABOX_TYPES)
    registry[key] = tuple(new_display_types)


def post_install(portal_setup):
    """Runs after the last import step of the *default* profile

    This handler is registered as a *post_handler* in the generic setup profile

    :param portal_setup: SetupTool
    """
    logger.info("SENAITE.DATABOX install handler [BEGIN]")

    # https://docs.plone.org/develop/addons/components/genericsetup.html#custom-installer-code-setuphandlers-py
    profile_id = "profile-senaite.databox:default"
    context = portal_setup._getImportContext(profile_id)
    portal = context.getSite()  # noqa

    logger.info("SENAITE.DATABOX install handler [DONE]")


def post_uninstall(portal_setup):
    """Runs after the last import step of the *uninstall* profile

    This handler is registered as a *post_handler* in the generic setup profile

    :param portal_setup: SetupTool
    """
    logger.info("SENAITE.DATABOX uninstall handler [BEGIN]")

    # https://docs.plone.org/develop/addons/components/genericsetup.html#custom-installer-code-setuphandlers-py
    profile_id = "profile-senaite.databox:uninstall"
    context = portal_setup._getImportContext(profile_id)
    portal = context.getSite()  # noqa

    logger.info("SENAITE.DATABOX uninstall handler [DONE]")
