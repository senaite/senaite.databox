# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.databox.behaviors.databox import IDataBoxBehavior
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
        portal_types = api.get_tool("portal_types")
        content_types = portal_types.listContentTypes()
        items = [
            SimpleTerm(item, item, item)
            for item in content_types
        ]
        return SimpleVocabulary(items)


QueryTypesVocabularyFactory = QueryTypesVocabulary()
