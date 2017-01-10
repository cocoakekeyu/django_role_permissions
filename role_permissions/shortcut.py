# -*- coding: utf-8 -*-
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from .models import Role
from .__init__ import get_role_model


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
    user = getattr(user, 'user', None) or user
    if user in role.group.user_set:
        return
    role.assign_role_to_user(user)


def remove_role(user, role):
    """
    移除用户角色
    """
    user = getattr(user, 'user', None) or user
    user.groups.clear()


def remove_roles(user):
    """
    移除用户所有角色
    """
    user = getattr(user, 'user', None) or user
    user.groups.clear()


def has_role(user, role):
    if user in role.group.user_set:
        return True
    return False


def get_user_roles(user):
    """
    获取用户所有角色
    """
    user = getattr(user, 'user', None) or user
    roles = Role.objects.filter(group__in=user.groups.all())
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
    return list(Permission.objects.filter(content_type=role_ct))


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


def get_or_create_permission(permission_name):
    role_ct = ContentType.objects.get_for_model(get_role_model())
    permission, created = Permission.objects.get_or_create(
        content_type=role_ct,
        codename=permission_name)
    return permission


def get_or_create_permissions(permission_names):
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