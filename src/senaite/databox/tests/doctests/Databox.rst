SENAITE DATABOX
===============

A databox acts like an intelligent folder with a stored database query that get
executed when showing the contents of the folder.

The query can be added by the user should be done in the following order:

  1. Search for a specific content type, e.g. "Sample" or "Patient"
  2. Select the schema columns that should be displayed
  3. Add a filter criteria, e.g. a daterange for the created date

The filter criteria can be also a schema field from a subquery, e.g. Samples
that contain a specific Analysis or Patient.

Sub queries execute another query and the display values can be matched against
the values from the parent query.

Maybe this requirement can be achieved by allowing databoxes in databoxes
(containment) and inheritance of the parent databox?


Test Setup
----------

Needed Imports:

    >>> from bika.lims import api
    >>> from DateTime import DateTime
    >>> from bika.lims.workflow import doActionFor as do_action_for
    >>> from bika.lims.utils.analysisrequest import create_analysisrequest

Setup the testing environment:

    >>> portal = self.portal
    >>> request = self.request
    >>> setup = portal.setup
    >>> bikasetup = portal.bika_setup
    >>> user = api.get_current_user()
    >>> date_now = DateTime().strftime("%Y-%m-%d")
    >>> date_future = (DateTime() + 5).strftime("%Y-%m-%d")
    >>> analysisservices = bikasetup.bika_analysisservices
    >>> labcontacts = bikasetup.bika_labcontacts
    >>> analysiscategories = bikasetup.bika_analysiscategories

Functional Helpers:

    >>> def start_server():
    ...     from Testing.ZopeTestCase.utils import startZServer
    ...     ip, port = startZServer()
    ...     return "http://{}:{}/{}".format(ip, port, portal.id)

    >>> def timestamp(format="%Y-%m-%d"):
    ...     return DateTime().strftime(format)

    >>> def new_ar(client, contact, sampletype, services, date_sampled=date_now, **kw):
    ...     values = {
    ...         'Client': client.UID(),
    ...         'Contact': contact.UID(),
    ...         'DateSampled': date_sampled,
    ...         'SampleType': sampletype.UID()}
    ...     service_uids = map(api.get_uid, services)
    ...     ar = create_analysisrequest(client, request, values, service_uids)
    ...     transitioned = do_action_for(ar, "receive")
    ...     return ar

    >>> def submit_analyses(ar):
    ...     for analysis in ar.getAnalyses(full_objects=True):
    ...         analysis.setResult(13)
    ...         do_action_for(analysis, "submit")

    >>> def verify_analyses(ar):
    ...     for analysis in ar.getAnalyses(full_objects=True):
    ...         do_action_for(analysis, "verify")



LIMS Setup
----------

Setup the Lab for testing:

    >>> bikasetup.setSelfVerificationEnabled(True)

    >>> client1 = api.create(portal.clients, "Client", Name="Happy Hills", ClientID="HH")
    >>> client2 = api.create(portal.clients, "Client", Name="Sunny Side", ClientID="SS")

    >>> contact1 = api.create(client1, "Contact", Firstname="Rita", Lastname="Mohale")
    >>> contact2 = api.create(client2, "Contact", Firstname="Sarel", Lastname="Seemonster")

    >>> labcontact1 = api.create(labcontacts, "LabContact", Firstname="Lab", Lastname="Contact 1")
    >>> labcontact2 = api.create(labcontacts, "LabContact", Firstname="Lab", Lastname="Contact 2")

    >>> sampletype1 = api.create(bikasetup.bika_sampletypes, "SampleType", title="Metals", Prefix="Metals")
    >>> sampletype2 = api.create(bikasetup.bika_sampletypes, "SampleType", title="Water", Prefix="Water")

    >>> department1 = api.create(setup.departments, "Department", title="Chemistry", Manager=labcontact1)
    >>> department2 = api.create(setup.departments, "Department", title="Microbiology", Manager=labcontact2)
    
    >>> category1 = api.create(analysiscategories, "AnalysisCategory", title="Metals", Department=department1)
    >>> category2 = api.create(analysiscategories, "AnalysisCategory", title="Microbiology", Department=department2)

    >>> Cu = api.create(analysisservices, "AnalysisService", title="Copper", Keyword="Cu", Price="15", Category=category1.UID(), Accredited=True)
    >>> Fe = api.create(analysisservices, "AnalysisService", title="Iron", Keyword="Fe", Price="10", Category=category1.UID())
    >>> Au = api.create(analysisservices, "AnalysisService", title="Gold", Keyword="Au", Price="20", Category=category1.UID())

Create some samples:

    >>> ar11 = new_ar(client1, contact1, sampletype1, [Cu, Fe, Au])
    >>> ar12 = new_ar(client1, contact1, sampletype1, [Cu, Fe])
    >>> ar13 = new_ar(client1, contact1, sampletype1, [Cu])

    >>> ar21 = new_ar(client2, contact2, sampletype1, [Cu, Fe, Au])
    >>> ar22 = new_ar(client2, contact2, sampletype1, [Cu, Fe])
    >>> ar23 = new_ar(client2, contact2, sampletype1, [Cu])
