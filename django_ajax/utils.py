# -*- coding: utf-8 -*-
"""
Utils
"""
from django.http.response import HttpResponseRedirectBase, HttpResponse
from django.template.response import TemplateResponse
from django.utils.encoding import force_unicode
from django.db.models.base import ModelBase

import json


class LazyJSONEncoder(json.JSONEncoder):
    """
    A JSONEncoder subclass that handle querysets and models objects.
    Add how handle your type of object here to use when when dump json
    """

    def default(self, obj):
        # handles HttpResponse and exception content
        if issubclass(type(obj), HttpResponseRedirectBase):
            return obj['Location']
        elif issubclass(type(obj), TemplateResponse):
            return obj.rendered_content
        elif issubclass(type(obj), HttpResponse):
            return obj.content
        elif issubclass(type(obj), Exception):
            return force_unicode(obj)

        # this handles querysets and other iterable types
        try:
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)

        # this handlers Models
        if isinstance(obj.__class__, ModelBase):
            return force_unicode(obj)

        return super(LazyJSONEncoder, self).default(obj)


def serialize_to_json(obj, *args, **kwargs):
    """
    A wrapper for simplejson.dumps with defaults as:

    cls=LazyJSONEncoder

    All arguments can be added via kwargs
    """

    kwargs['cls'] = kwargs.get('cls', LazyJSONEncoder)

    return json.dumps(obj, *args, **kwargs)
