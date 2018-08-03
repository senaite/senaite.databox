# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.DATABOX
#
# Copyright 2018 by it's authors.

from senaite import api
from senaite.databox.config import NOT_ADDABLE_TYPES
from zope.interface import directlyProvides
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def get_addable_types():
    """returns a list portal types (name, title) pairs
    """
    portal_types = api.get_tool("portal_types")
    portal_properties = api.get_tool("portal_properties")
    site_properties = portal_properties.site_properties

    not_searched = site_properties.getProperty("types_not_searched", [])
    types_dict = portal_types.listTypeTitles()

    searchable_types = filter(lambda t: t not in not_searched,
                              types_dict)

    addable_types = filter(lambda t: t not in NOT_ADDABLE_TYPES,
                           searchable_types)

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
