# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import wraps

from django.core.exceptions import PermissionDenied
from .shortcut import has_roles


def required_roles(roles):
    def required_decorator(fuc):
        @wraps(fuc)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if not has_roles(user, roles):
                raise PermissionDenied
            return fuc(request, *args, **kwargs)
        return wrapper
    return required_decorator
