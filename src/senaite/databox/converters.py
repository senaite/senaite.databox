# -*- coding: utf-8 -*-

import six

from bika.lims import api
from bika.lims.utils import get_link
from DateTime import DateTime
from plone.protect.utils import addTokenToUrl
from Products.ATContentTypes.utils import DT2dt

LINK_TO_PARENT_TYPES = [
    "Analysis",
]


def to_string(obj, key, value, **kw):
    """to string
    """
    if isinstance(value, six.string_types):
        value = api.safe_unicode(value).encode("utf-8")
    if value is None:
        value = ""
    return str(value)


def to_link(obj, key, value, **kw):
    """to link
    """
    value = to_string(obj, key, value)
    if not value:
        return ""
    if api.get_portal_type(obj) in LINK_TO_PARENT_TYPES:
        obj = api.get_parent(obj)
    url = addTokenToUrl(api.get_url(obj))
    return get_link(url, value)


def to_date(obj, key, value, dfmt="%d.%m.%Y"):
    """to date
    """
    if not isinstance(value, DateTime):
        return ""
    return DT2dt(value).strftime(dfmt)


def to_long_date(obj, key, value, dfmt="%d.%m.%Y %H:%M"):
    """to long date
    """
    return to_date(obj, key, value, dfmt=dfmt)
