# -*- coding: utf-8 -*-

import os

import transaction
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import login
from plone.app.testing import logout
from plone.testing import zope
from senaite.core.exportimport.load_setup_data import LoadSetupData


class BaseLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(BaseLayer, self).setUpZope(app, configurationContext)

        # Load ZCML
        import Products.TextIndexNG3
        import bika.lims
        import senaite.core
        import senaite.core.listing
        import senaite.core.spotlight
        import senaite.impress
        import senaite.lims
        import senaite.databox

        # XXX Hack to avoid this bug:
        # IOError: [Errno 2] No such file or directory:
        #          '.../senaite.core.supermodel/src/senaite/core/configure.zcml'
        # Call Stack:
        # plone.app.testing.helpers.loadZCML
        # zope.configuration.xmlconfig.file
        # zope.configuration.xmlconfig.include
        # zope.configuration.config.ConfigurationContext.path
        # zope.configuration.config.ConfigurationContext.processxmlfile
        senaite.core.__path__ = [os.path.dirname(senaite.core.__file__)]

        self.loadZCML(package=Products.TextIndexNG3)
        self.loadZCML(package=bika.lims)
        self.loadZCML(package=senaite.core)
        self.loadZCML(package=senaite.core.listing)
        self.loadZCML(package=senaite.core.spotlight)
        self.loadZCML(package=senaite.impress)
        self.loadZCML(package=senaite.lims)

        # Install product and call its initialize() function
        zope.installProduct(app, "Products.TextIndexNG3")
        zope.installProduct(app, "bika.lims")
        zope.installProduct(app, "senaite.core")
        zope.installProduct(app, "senaite.core.listing")
        zope.installProduct(app, "senaite.core.spotlight")
        zope.installProduct(app, "senaite.impress")
        zope.installProduct(app, "senaite.lims")
        zope.installProduct(app, "senaite.databox")

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, "senaite.core:default")
        applyProfile(portal, "senaite.databox:default")
        transaction.commit()


class DataLayer(BaseLayer):
    """Layer including Demo Data
    """

    def setup_data_load(self, portal, request):
        login(portal.aq_parent, SITE_OWNER_NAME)

        # load test data
        request.form["setupexisting"] = 1
        request.form["existing"] = "bika.lims:test"
        lsd = LoadSetupData(portal, request)
        lsd()
        logout()

    def setUpPloneSite(self, portal):
        super(DataLayer, self).setUpPloneSite(portal)

        # Install Demo Data
        self.setup_data_load(portal, portal.REQUEST)


BASE_LAYER_FIXTURE = BaseLayer()
BASE_TESTING = FunctionalTesting(
    bases=(BASE_LAYER_FIXTURE,), name="SENAITE.DATABOX:BaseTesting")

DATA_LAYER_FIXTURE = DataLayer()
DATA_TESTING = FunctionalTesting(
    bases=(DATA_LAYER_FIXTURE,), name="SENAITE.DATABOX:DataTesting")
