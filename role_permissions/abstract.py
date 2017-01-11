# -*- coding: utf-8 -*-
from .shortcut import get_or_create_permissions, get_or_create_permission
from .exceptions import InitPermissionError
from .utils import get_role_model
from django.core.exceptions import ObjectDoesNotExist


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
            role = get_role_model().objects.get(name=name)
        except ObjectDoesNotExist:
            role = get_role_model().objects.create(name=name, **extra)

        return role


class AbstractPermissonMetaclass(type):
    def __new__(cls, name, bases, dct):
        permission_class = type.__new__(cls, name, bases, dct)
        category = dct.get('category', name)
        if 'perms' not in dct:
            raise InitPermissionError('perms must be exists')
        perms = dct['perms']
        cls._create_permissions(perms, category)
        print('test')
        return permission_class

    @classmethod
    def _create_permissions(cls, perms, category):
        cls._check_perms_config(perms)
        for perm in perms:
            perm['category'] = category
            get_or_create_permission(**perm)

    @classmethod
    def _check_perms_config(cls, perms):
        pass


class AbstractPermisson(object):

    __metaclass__ = AbstractPermissonMetaclass
