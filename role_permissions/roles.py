# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist

from .models import Role
from .shortcut import get_or_create_permissions


registerd_roles = {}


class AbstractRoleMetaclass(type):
    def __new__(cls, name, bases, dct):
        role_class = type.__new__(cls, name, bases, dct)
        registerd_roles[role_class.get_name()] = role_class
        return role_class


class AbstractRole(object):

    __metaclass__ = AbstractRoleMetaclass

    def __new__(cls, *args, **kwargs):
        if hasattr(cls, 'name'):
            name = cls.name
        else:
            name = cls.__name__

        extra = {}

        if hasattr(cls, 'permissions'):
            permissions = get_or_create_permissions(cls.permissions)
            extra['permissions'] = permissions

        try:
            role = Role.objects.get(name=name)
        except ObjectDoesNotExist:
            role = Role.objects.create(name=name, **extra)

        return role