# -*- coding: utf-8 -*-
from django.conf import settings
from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .models import Role, PermissionGroup


def get_role_model():
    """
    Returns the Role model that is active in this project.
    """
    try:
        return django_apps.get_model(settings.AUTH_ROLE_MODEL)
    except ValueError:
        raise ImproperlyConfigured(
            "AUTH_ROLE_MODEL must be of the form 'app_label.model_name'")
    except (LookupError, AttributeError):
        return Role


def get_or_create_permission(codename, name=None, category='default'):
    role_ct = ContentType.objects.get_for_model(get_role_model())
    defaults = {}
    name = name or codename
    defaults.update({'name': name})
    permission, created = Permission.objects.get_or_create(
        content_type=role_ct,
        codename=codename,
        defaults=defaults)
    if created:
        PermissionGroup.objects.create(permission=permission, name=category)

    return permission


def get_or_create_permissions(permission_names):
    role_ct = ContentType.objects.get_for_model(get_role_model())
    permissions = list(Permission.objects.filter(
        content_type=role_ct, codename__in=permission_names).all())

    if len(permissions) != len(permission_names):
        for permission_name in permission_names:
            permission, created = Permission.objects.get_or_create(
                content_type=role_ct,
                codename=permission_name,
                defaults={'name': permission_name})
            if created:
                permissions.append(permission)
                PermissionGroup.objects.create(permission=permission)

    return permissions


def get_or_create_role(name, permissions=None):
    manager = get_role_model().objects
    try:
        return manager.get(name=name)
    except manager.model.DoesNotExist:
        return manager.create(name=name, permissions=permissions)
