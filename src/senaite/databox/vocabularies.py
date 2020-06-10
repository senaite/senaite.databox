# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.databox.config import ADDABLE_TYPES
from zope.interface import directlyProvides
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


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
