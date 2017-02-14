# -*- coding: utf-8 -*-
import inspect

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from .models import PermissionGroup
from .utils import get_role_model
from role_permissions.abstract import AbstractRole


# Role operate


def assign_roles(user, roles):
    """
    给用户分配角色
    """
    remove_roles(user)
    for role in roles:
        role.assign_role_to_user(user)


def add_role(user, role):
    """
    给用户添加一个角色
    """
    if issubclass(role, AbstractRole):
        role = role.get_registered_role()
    if user in role.group.user_set.all():
        return
    role.assign_role_to_user(user)


def remove_role(user, role):
    """
    移除用户角色
    """
    user.groups.clear()


def remove_roles(user):
    """
    移除用户所有角色
    """
    user.groups.clear()


def has_role(user, role):
    if user and user.is_superuser:
        return True

    user_roles = get_user_roles(user)

    if not user_roles:
        return False

    if inspect.isclass(role):
        role = role.get_registered_role()
    elif not isinstance(role, get_role_model()):
        role = get_role_model().objects.get(name=role)

    return role in user_roles


def has_roles(user, roles):

    if user and user.is_superuser:
        return True

    user_roles = get_user_roles(user)

    if not user_roles:
        return False

    if not isinstance(roles, list):
        roles = [roles]

    normalized_roles = []
    for role in roles:
        if inspect.isclass(role):
            role = role.get_registered_role()
        elif not isinstance(role, get_role_model()):
            role = get_role_model().objects.get(name=role)
        normalized_roles.append(role)

    return set(normalized_roles).issubset(user_roles)


def get_user_roles(user):
    """
    获取用户所有角色
    """
    roles = get_role_model().objects.filter(group__in=user.groups.all())
    return list(roles)


def get_user_role(user):
    """
    获取用户一个角色
    """
    roles = get_user_roles(user)
    return roles[0] if roles else None


# Permissions


def get_all_permissions():
    role_ct = ContentType.objects.get_for_model(get_role_model())
    return list(Permission.objects.filter(
        content_type=role_ct).exclude(name__startswith='Can'))


def get_permission(permission_name):
    role_ct = ContentType.objects.get_for_model(get_role_model())
    try:
        permission = Permission.objects.get(
            content_type=role_ct, codename=permission_name)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist('未找到对应的权限')
    return permission


def get_permissions(permission_names):
    role_ct = ContentType.objects.get_for_model(get_role_model())
    permissions = Permission.objects.filter(
        content_type=role_ct, codename__in=permission_names)
    if len(permissions) < len(permission_names):
        raise ObjectDoesNotExist('未找到对应的权限')


def get_user_permissions(user):
    role_ct = ContentType.objects.get_for_model(get_role_model())
    permissions = Permission.objects.filter(
        content_type=role_ct, group__in=user.groups.all())
    return permissions
