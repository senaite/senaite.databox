# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.databox.behaviors.databox import IDataBoxBehavior
from senaite.databox.config import ADDABLE_TYPES
from zope.interface import directlyProvides
from zope.interface import implementer
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class DisplayColumnsVocabulary(object):
    """Returns all available fields of the selected type
    """
    def __call__(self, context):
        adapted = IDataBoxBehavior(context)
        items = [
            SimpleTerm(field, field, field)
            for field in adapted.get_fields()
        ]
        return SimpleVocabulary(items)


DisplayColumnsVocabularyFactory = DisplayColumnsVocabulary()


@implementer(IVocabularyFactory)
class QueryTypesVocabulary(object):

    def __call__(self, context):
        import pdb; pdb.set_trace()
        items = []
        return SimpleVocabulary(items)


QueryTypesVocabularyFactory = QueryTypesVocabulary()


def get_addable_types():
    """returns a list portal types (name, title) pairs
    """
    portal_types = api.get_tool("portal_types")
    types_dict = portal_types.listTypeTitles()
    addable_types = filter(lambda t: t in types_dict, ADDABLE_TYPES)
    return map(lambda t: (t, types_dict[t]), sorted(addable_types))


def addable_types_vocabulary(context):
    """Vocabulary of addable types
    """
    terms = []
    addable_types = get_addable_types()
    for name, title in addable_types:
        term = SimpleTerm(value=name, title=title)
        terms.append(term)
    return SimpleVocabulary(terms)


directlyProvides(addable_types_vocabulary, IContextSourceBinder)
