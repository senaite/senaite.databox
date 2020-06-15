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
    return get_link(api.get_url(obj), to_string(obj, key, value))


def to_date(obj, key, value, format="%d.%m.%y"):
    if not isinstance(value, DateTime):
        return ""
    return DT2dt(value).strftime(format)


def to_long_date(obj, key, value, format="%d.%m.%y"):
    return to_date(obj, key, value, format="%d.%m.%y %H:%M")
