# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .decorators import required_roles


class RequiredRoleMixin(object):
    allowed_roles = []

    @required_roles(allowed_roles)
    def dispatch(self, request, *args, **kwargs):
        return super(RequiredRoleMixin, self).dispatch(
            request, *args, **kwargs)
