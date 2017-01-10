# -*- coding: utf-8 -*-
from .models import Role
from .shortcut import get_role_model

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
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
            permissions = cls.get_or_create_permissions(cls.permissions)
            extra['permissions'] = permissions

        # role = Role.objects.get_or_create(name=name, defaults=extra)
        try:
            role = Role.objects.get(name=name)
        except ObjectDoesNotExist:
            role = Role.objects.create(name=name, **extra)

        return role

    @classmethod
    def get_or_create_permissions(cls, permission_names):
        role_ct = ContentType.objects.get_for_model(get_role_model())
        permissions = list(Permission.objects.filter(
            content_type=role_ct, codename__in=permission_names).all())

        if len(permissions) != len(permission_names):
            for permission_name in permission_names:
                permission, created = Permission.objects.get_or_create(
                    content_type=role_ct, codename=permission_name)
                if created:
                    permissions.append(permission)

        return permissions
