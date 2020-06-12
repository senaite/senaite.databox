# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.databox.behaviors.databox import IDataBoxBehavior
from senaite.databox.config import NON_QUERYABLE_TYPES
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class DisplayColumnsVocabulary(object):
    """Returns all available fields of the selected type
    """
    def __call__(self, context):
        adapted = IDataBoxBehavior(context, None)
        if adapted is None:
            return SimpleVocabulary([])
        items = [
            SimpleTerm(field, field, field)
            for field in adapted.get_fields()
        ]
        return SimpleVocabulary(items)


DisplayColumnsVocabularyFactory = DisplayColumnsVocabulary()


@implementer(IVocabularyFactory)
class QueryTypesVocabulary(object):

    def __call__(self, context):
        portal_state = api.get_view("plone_portal_state")
        content_types = portal_state.friendly_types()
        # filter out non queryable types
        content_types = filter(
            lambda pt: pt not in NON_QUERYABLE_TYPES, content_types)
        items = [
            SimpleTerm(item, item, item)
            for item in content_types
        ]
        return SimpleVocabulary(items)


QueryTypesVocabularyFactory = QueryTypesVocabulary()
