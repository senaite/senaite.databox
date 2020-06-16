# -*- coding: utf-8 -*-

import six

from bika.lims import api
from bika.lims.utils import get_link
from DateTime import DateTime
from Products.ATContentTypes.utils import DT2dt


def to_string(obj, key, value, **kw):
    if isinstance(value, six.string_types):
        value = value.encode("utf-8")
    if value is None:
        value = ""
    return str(value)


def to_link(obj, key, value, **kw):
    """Gnerate hyperlink to object
    """
    value = to_string(obj, key, value)
    if not value:
        return ""
    return get_link(api.get_url(obj), value)


def to_date(obj, key, value, dfmt="%d.%m.%Y"):
    if not isinstance(value, DateTime):
        return ""
    return DT2dt(value).strftime(dfmt)


def to_long_date(obj, key, value, dfmt="%d.%m.%Y %H:%M"):
    return to_date(obj, key, value, dfmt=dfmt)
