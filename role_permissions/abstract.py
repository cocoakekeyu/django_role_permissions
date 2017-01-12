# -*- coding: utf-8 -*-
from six import add_metaclass

from django.core.exceptions import ObjectDoesNotExist

from .shortcut import get_or_create_permissions, get_or_create_permission
from .exceptions import InitPermissionError
from .utils import get_role_model
from .exceptions import RoleDoesNotRegister


registered_roles = {}


class AbstractRole(object):

    def __new__(cls, *args, **kwargs):
        try:
            role = cls.get_registered_role()
        except RoleDoesNotRegister:
            if hasattr(cls, 'name'):
                name = cls.name
            else:
                name = cls.__name__
            extra = {}
            if hasattr(cls, 'permissions'):
                permissions = get_or_create_permissions(cls.permissions)
                extra['permissions'] = permissions

            role = get_role_model().objects.create(name=name, **extra)
            registered_roles[cls.__name__] = role

        return role

    @classmethod
    def get_registered_role(cls):
        name = cls.__name__
        if name in registered_roles:
            return registered_roles[name]
        else:
            raise RoleDoesNotRegister()


class AbstractPermissonMetaclass(type):
    def __new__(cls, name, bases, dct):
        permission_class = type.__new__(cls, name, bases, dct)
        if name != 'AbstractPermisson':
            category = dct.get('category', name)
            if 'perms' not in dct:
                raise InitPermissionError('perms must be exists')
            perms = dct['perms']
            cls._create_permissions(perms, category)

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


@add_metaclass(AbstractPermissonMetaclass)
class AbstractPermisson(object):
    pass
